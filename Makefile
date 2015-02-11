MKDIR_P = mkdir -p

default:
	@make test

build:
	@gradle build

test:
	@make build
	@gradle test

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
	@gradle clean

		
