from setuptools import setup

if __name__ == "__main__":
    try:
        setup(
            use_scm_version={"version_scheme": "no-guess-dev"},
            name='docker_hub',
            packages=['docker_hub', ],
            entry_points={
                'console_scripts': [
                    'docker_hub=docker_hub.main:main',
                ]
            },
            install_requires=[
                # "requests==2.28.0",
                # "tabulate==0.8.10",
                # "python-dateutil==2.8.2",
            ],
            data_files=[
                # ('', ['src/abc/config.sample.yaml']),
            ]

        )
    except:  # noqa
        print(
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of setuptools, "
            "setuptools_scm and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise
