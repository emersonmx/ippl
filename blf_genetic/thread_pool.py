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

import copy

from Queue import Queue
from threading import Thread


class Worker(Thread):

    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            function, args, kwargs = self.tasks.get()
            try: function(*args, **kwargs)
            except Exception, e: print e
            self.tasks.task_done()


class ThreadPool(object):

    def __init__(self, jobs, blf_data):
        super(ThreadPool, self).__init__()

        self.data_queue = []
        for _ in xrange(jobs):
            self.data_queue.append(copy.deepcopy(blf_data))

        self.tasks = Queue(jobs)
        for _ in xrange(jobs):
            Worker(self.tasks)

    def add_task(self, function, *args, **kwargs):
        self.tasks.put((function, args, kwargs))

    def wait_completion(self):
        self.tasks.join()

