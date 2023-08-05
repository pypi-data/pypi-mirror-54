
quisk2:
	python setup.py build_ext --force --inplace
	@echo
	@echo 'Use "make soapy" to make the Python2 soapy module'

quisk3:
	python3 setup.py build_ext --force --inplace
	@echo
	@echo 'Use "make soapy3" to make the Python3 soapy module'

soapy:
	(cd soapypkg; make soapy2)

soapy3:
	(cd soapypkg; make soapy3)

macports:
	env ARCHFLAGS="-arch x86_64" python setup.py build_ext --force --inplace -D USE_MACPORTS
