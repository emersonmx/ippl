from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension("lib2dipp/bottom_left_fill/algorithm", [
        "lib2dipp/bottom_left_fill/algorithm.py"
    ]),
    Extension("lib2dipp/bottom_left_fill/sheet_shape", [
        "lib2dipp/bottom_left_fill/sheet_shape.py"
    ]),
    Extension("lib2dipp/drawer/drawer", [
        "lib2dipp/drawer/drawer.py"
    ]),
    Extension("lib2dipp/genetic_algorithm/application", [
        "lib2dipp/genetic_algorithm/application.py"
    ]),
    Extension("lib2dipp/genetic_algorithm/chromosome", [
        "lib2dipp/genetic_algorithm/chromosome.py"
    ]),
    Extension("lib2dipp/genetic_algorithm/crossover", [
        "lib2dipp/genetic_algorithm/crossover.py"
    ]),
    Extension("lib2dipp/genetic_algorithm/mutation", [
        "lib2dipp/genetic_algorithm/mutation.py"
    ]),
    Extension("lib2dipp/reader", [
        "lib2dipp/reader.py"
    ]),
    Extension("lib2dipp/render", [
        "lib2dipp/render.py"
    ]),
    Extension("lib2dipp/shape/arc", [
        "lib2dipp/shape/arc.py"
    ]),
    Extension("lib2dipp/shape/base", [
        "lib2dipp/shape/base.py"
    ]),
    Extension("lib2dipp/shape/line", [
        "lib2dipp/shape/line.py"
    ]),
    Extension("lib2dipp/shape/loop", [
        "lib2dipp/shape/loop.py"
    ]),
    Extension("lib2dipp/shape/point", [
        "lib2dipp/shape/point.py"
    ]),
    Extension("lib2dipp/shape/rectangle", [
        "lib2dipp/shape/rectangle.py"
    ]),
    Extension("lib2dipp/shape/shape", [
        "lib2dipp/shape/shape.py"
    ]),
    Extension("lib2dipp/util", [
        "lib2dipp/util.py"
    ])
]

setup(
  name = 'lib2dipp',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)
