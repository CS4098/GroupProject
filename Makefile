MKDIR_P = mkdir -p
PML_BNFC = pml-bnfc

default:
	@make test

build:
	if [ ! -d ${PML_BNFC} ]; then ${MKDIR_P} ${PML_BNFC} && hg clone https://PinPinIre@bitbucket.org/PinPinIre/pml-bnfc ${PML_BNFC}; fi
	@cd ${PML_BNFC}/xml && make

test:
	@make build
	@./test-suite/runner-translator.sh ./src/main/translator-xml/PMLToPromela.sh ./test-suite/translator-inputs
	@./src/test/uitest/runtest.sh

install:
ifdef DESTDIR
	if [ ! -d ${DESTDIR} ]; then ${MKDIR_P} ${DESTDIR}; fi
	@make build 
	@cp -r target/* ${DESTDIR}
	@cp -r src/main/webapp/ ${DESTDIR}/public_html
else
	@echo DESTDIR not set
endif

clean:
	@rm -rf ${PML_BNFC}

		
