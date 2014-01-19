from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension("ippl/bottom_left_fill/algorithm", [
        "ippl/bottom_left_fill/algorithm.py"
    ]),
    Extension("ippl/bottom_left_fill/sheet_shape", [
        "ippl/bottom_left_fill/sheet_shape.py"
    ]),
    Extension("ippl/drawer/drawer", [
        "ippl/drawer/drawer.py"
    ]),
    Extension("ippl/genetic_algorithm/application", [
        "ippl/genetic_algorithm/application.py"
    ]),
    Extension("ippl/genetic_algorithm/chromosome", [
        "ippl/genetic_algorithm/chromosome.py"
    ]),
    Extension("ippl/genetic_algorithm/crossover", [
        "ippl/genetic_algorithm/crossover.py"
    ]),
    Extension("ippl/genetic_algorithm/mutation", [
        "ippl/genetic_algorithm/mutation.py"
    ]),
    Extension("ippl/reader", [
        "ippl/reader.py"
    ]),
    Extension("ippl/render", [
        "ippl/render.py"
    ]),
    Extension("ippl/shape/arc", [
        "ippl/shape/arc.py"
    ]),
    Extension("ippl/shape/base", [
        "ippl/shape/base.py"
    ]),
    Extension("ippl/shape/line", [
        "ippl/shape/line.py"
    ]),
    Extension("ippl/shape/loop", [
        "ippl/shape/loop.py"
    ]),
    Extension("ippl/shape/point", [
        "ippl/shape/point.py"
    ]),
    Extension("ippl/shape/rectangle", [
        "ippl/shape/rectangle.py"
    ]),
    Extension("ippl/shape/shape", [
        "ippl/shape/shape.py"
    ]),
    Extension("ippl/util", [
        "ippl/util.py"
    ])
]

setup(
  name = 'ippl',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)
