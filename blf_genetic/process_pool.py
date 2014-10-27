#
# Copyright (C) 2014 Emerson Max de Medeiros Silva
#
# This file is part of ippl.
#
# ippl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ippl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ippl.  If not, see <http://www.gnu.org/licenses/>.
#

from multiprocessing import Process
from multiprocessing import JoinableQueue
from multiprocessing import Manager


class Worker(Process):

    def __init__(self, queue):
        super(Worker, self).__init__()

        self.queue = queue
        self.daemon = True
        self.start()

    def run(self):
        while True:
            function, args, kwargs = self.queue.get()
            try: function(*args, **kwargs)
            except Exception, e: print e
            self.queue.task_done()


class ProcessPool(object):

    def __init__(self, jobs):
        super(ProcessPool, self).__init__()

        self.queue = JoinableQueue(jobs)

        for _ in xrange(jobs):
            Worker(self.queue)

    def add_process(self, func, *args, **kwargs):
        self.queue.put((func, args, kwargs))

    def wait_completion(self):
        self.queue.join()


