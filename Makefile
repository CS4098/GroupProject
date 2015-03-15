MKDIR_P = mkdir -p
PML_BNFC = pml-bnfc

default:
	@make test

build:
	if [ ! -d ${PML_BNFC} ]; then ${MKDIR_P} ${PML_BNFC} && hg clone https://PinPinIre@bitbucket.org/PinPinIre/pml-bnfc ${PML_BNFC}; fi
	@cabal sandbox init
	@cabal install
	@cp .cabal-sandbox/bin/Pmlxml ./pml-bnfc/xml/

test:
	@make build
	@./test-suite/runner-translator.sh ./src/main/translator-xml/PMLToPromela.sh ./test-suite/translator-inputs
	@./src/test/uitest/runtest.sh 2>&1 | grep -v "INFO"

clean:
	@rm -rf ${PML_BNFC}

		
