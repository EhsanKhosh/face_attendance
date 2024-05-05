import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

__version__ = "0.0.0"

setuptools.setup(
    name="faceAttendance",
    version=__version__,
    author="Ehsan Khosh",
    author_email="ehsan.khoshakhlagh77@gmail.com",
    description="Face Attendance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EhsanKhosh/faceAttendance",
    project_urls={
        'Issues' : 'https://github.com/EhsanKhosh/faceAttendance/issues'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    package_dir={'':'src'},
    packages=setuptools.find_packages(where='src')
)
    
    