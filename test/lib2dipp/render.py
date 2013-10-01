import PIL

import lib2dipp


class Render(object):

    def __init__(self):
        super(Render, self).__init__()

        self._image = None
        self._image_drawer = None

    def _calculate_size(self, shape):
        pass

    def _line(self, line):
        pass

    def _arc(self, arc):
        pass

    def shape(self, shape):
        pass

    def save(self, file_name):
        pass

if __name__ == '__main__':
    render = Render()

