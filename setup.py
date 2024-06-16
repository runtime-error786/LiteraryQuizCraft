from setuptools import find_packages,setup

setup(
    name="Mcq_Generator",
    version='0.0.1',
    author='Mustafa Rizwan',
    author_email='mustafa782a@gmail.com',
    install_requires=['openai','langchain','streamlit','python-dotenv','PyPDF2'],
    packages=find_packages()
)
