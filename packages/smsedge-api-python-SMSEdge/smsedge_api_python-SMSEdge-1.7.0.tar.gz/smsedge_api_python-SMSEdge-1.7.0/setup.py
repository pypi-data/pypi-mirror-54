import setuptools

setuptools.setup(
    name="smsedge_api_python-SMSEdge",
    packages=setuptools.find_packages(),
    version="1.7.0",
    author="Mimon Copitman",
    author_email="mimon@smsedge.io",
    description="SMSEdge API package for Python development",
    long_description_content_type="text/markdown",
    url="https://github.com/SMSEdge/API-Python",
    install_requires=[
        'requests',
        'cerberus',
        'datetime'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],

    python_requires='>=3.6',
)
