import setuptools

from glob import glob
import os


def get_path_files(path):
    all_files = []
    path_files = []
    for f_path in glob(os.path.join(path, '*')):
        if os.path.isdir(f_path):
            all_files += get_path_files(f_path)
        elif f_path[-3:] != '.py':
            path_files.append(f_path)

    all_files += [(path, path_files)]
    return all_files


path = os.path.join('jupyterlab_commenting_service')
extra_files = get_path_files(path)

setuptools.setup(
    name="jupyterlab_commenting_service",
    version='0.1',
    license='BSD-3-Clause',
    author='CalPoly/Quansight',
    author_email='jacobrhoussian@gmail.com',
    url='https://github.com/jupyterlab/jupyterlab-commenting',
    # py_modules rather than packages, since we only have 1 file
    packages=['jupyterlab_commenting_service'],
    entry_points={
        'jupyter_serverproxy_servers': [
            # name = packagename:function_name
            'comments = jupyterlab_commenting_service.service:start',
            'commenting-service = jupyterlab_commenting_service.service:fastapi',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    install_requires=['jupyter-server-proxy', 'fastapi[all]', 'datasette'],
    package_data=dict(extra_files),
    include_package_data=True
)
