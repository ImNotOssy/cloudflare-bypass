from setuptools import setup, find_packages

setup(
    name='cloudflare_bypass',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'opencv-python',
        'numpy',
        'Pillow',
        'pyautogui'
    ],
    package_data={
        'cloudflare_bypass': ['images/*.png', 'images/*.gif'],
    },
)
