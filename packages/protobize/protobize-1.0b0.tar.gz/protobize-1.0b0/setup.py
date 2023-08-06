from setuptools import setup

setup(
	name='protobize',
	version='1.0-beta',
	license = 'GNU Affero General Public License v3.0',

	author="Pierlauro Sciarelli",
	author_email="foss@pstux.dev",

	description='Compile protobuffers at package build time',

	url='https://github.com/pierlauro/protobize',

	py_modules=['protobize'],
	entry_points = {
		"distutils.commands": [
			"protobize = protobize:CompileProtoBuffers",
		],
	}
)
