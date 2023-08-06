import datetime
import logging
import sys

import fs.filesize

from ..importers.work_queue import Task, WorkQueue
from ..importers.progress_reporter import ProgressReporter
from ..util import confirmation_prompt


MAX_QUEUE_SIZE = 100000

log = logging.getLogger(__name__)


class SyncQueue(WorkQueue):
    def __init__(self, dst, jobs, assume_yes=False, dry_run=False):
        super().__init__({'store': jobs, 'delete': 1})
        self.dst = dst
        self.assume_yes = assume_yes
        self.dry_run = False
        self.cleanup = False
        self.report = SyncProgressReporter(self)
        self.report.add_group('store', 'Syncing', 0)
        self.report.add_group('delete', 'Deleting', 0)

    @property
    def full(self):
        return sum(len(queue) for queue in self.waiting.values()) > MAX_QUEUE_SIZE

    def store(self, src_file):
        self.enqueue(StoreTask(self, src_file))
        self.report.groups['store'].total_bytes += src_file.size

    def delete(self, dst_file):
        self.enqueue(DeleteTask(self, dst_file))
        self.cleanup = True

    def enqueue(self, task, priority=10):
        super().enqueue(task, priority=priority)
        self.report.groups[task.group].total_count += 1

    def confirm(self, message):
        if self.assume_yes:
            return True
        with self._lock:
            self.report.suspend()
            confirm = confirmation_prompt(message)
            self.report.resume()
            return confirm

    def start(self):
        super().start()
        self.report.start()

    def shutdown(self):
        if self.cleanup:
            self.dst.cleanup()
        self.report.shutdown()
        self.report.final_report()
        super().shutdown()


class StoreTask(Task):
    __slots__ = ('queue', 'src_file', 'bytes_read')

    def __init__(self, queue, src_file):
        super().__init__('store')
        self.queue = queue
        self.src_file = src_file
        self.bytes_read = 0

    def execute(self):
        """Store source file on destination (or skip if already up to date)"""
        dst_file = self.queue.dst.file(self.src_file.name)
        if not dst_file.stat():
            self.store('create', dst_file)
        elif self.src_file.size == dst_file.size and self.src_file.modified <= dst_file.modified:
            self.skip('stat')
        elif self.queue.confirm(f'Are you sure you want to replace "{self.src_file.name}"?'):
            self.store('update', dst_file)
        else:
            self.skip('user')
        return None, None

    def store(self, event, dst_file):
        log.debug(f'{event} {self.src_file.name}')
        if not self.queue.dry_run:
            dst_file.store(self.src_file)
            self.bytes_read = self.src_file.bytes_read
            self.src_file.cleanup()
            self.src_file = None

    def skip(self, event):
        log.debug(f'skip/{event} {self.src_file.name}')
        self.queue.skip_task(task=self)
        self.skipped = True

    def get_bytes_processed(self):
        """Return number of bytes read from the source (equals bytes written to destination)"""
        return self.bytes_read

    def get_desc(self):
        """store path/to/file"""
        return f'{self.group} {self.src_file.name}'


class DeleteTask(Task):
    __slots__ = ('queue', 'dst_file')

    def __init__(self, queue, dst_file):
        super().__init__('delete')
        self.queue = queue
        self.dst_file = dst_file

    def execute(self):
        """Delete file on destination"""
        log.debug(self.get_desc())
        if not self.queue.dry_run:
            self.dst_file.delete()
        return None, None

    def get_bytes_processed(self):
        """Return one (representing a single file instead of bytes)"""
        return 1

    def get_desc(self):
        """delete path/to/file"""
        return f'{self.group} {self.dst_file.name}'


class SyncProgressReporter(ProgressReporter):
    def report(self, newline='\r'):
        messages = []
        for name, group in self.groups.items():
            total_count = group.total_count - group.skipped
            if total_count > 0:
                if group.completed == total_count:
                    speed_str = 'DONE'
                elif name == 'store':
                    speed_str = fs.filesize.traditional(group.bytes_per_sec) + '/s'
                elif name == 'delete':
                    # NOTE reusing group.bytes_per_sec for tracking deleted / sec
                    # TODO in-depth subclassing of WorkQueue for appropriate attribute name
                    speed_str = f'{group.bytes_per_sec:.2f}/s'
                messages.append(f'{group.desc} {group.completed}/{group.total_count} - {speed_str}')
        message = ', '.join(messages).ljust(self.columns) + newline
        sys.stdout.write(message)
        sys.stdout.flush()

    def final_report(self):
        self.sample()
        self.report(newline='\n')
        if self.groups['store'].completed > self.groups['store'].skipped:
            xfer_bytes = fs.filesize.traditional(self.groups['store'].completed_bytes)
            xfer_time = self.format_timedelta(datetime.datetime.now() - self._start_time)
            print(f'Transferred {xfer_bytes} in {xfer_time}')
        if self.groups['store'].skipped > 0:
            skipped_count = self.groups['store'].skipped
            print(f'Skipped {skipped_count} files')
        if self.groups['delete'].completed > 0:
            deleted_count = self.groups['delete'].completed
            print(f'Deleted {deleted_count} files')

    @staticmethod
    def format_timedelta(timedelta):
        """Return human-readable str given a datetime.timedelta"""
        seconds = timedelta.total_seconds()
        if seconds < 60:
            return f'{seconds:.2f} seconds'
        return str(datetime.timedelta(seconds=int(seconds)))
