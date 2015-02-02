default:
	@make test

build:
	@mvn validate compile

test:
	@make build
	@mvn test

install:
ifdef DESTDIR
	@make build 
	@cp -r target/* ${DESTDIR}
	@cp -r src/main/webapp/ ${DESTDIR}/public_html
else
	@echo DESTDIR not set
endif

clean:
	@mvn clean

		
