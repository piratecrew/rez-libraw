
SHELL := /bin/bash

# Rez variables, setting these to sensible values if we are not building from rez
REZ_BUILD_PROJECT_VERSION ?= NOT_SET
REZ_BUILD_INSTALL_PATH ?= /usr/local
REZ_BUILD_SOURCE_PATH ?= $(shell dirname $(lastword $(abspath $(MAKEFILE_LIST))))
BUILD_ROOT := $(REZ_BUILD_SOURCE_PATH)/build
REZ_BUILD_PATH ?= $(BUILD_ROOT)
REZ_JPEGTURBO_ROOT ?= /usr/local

# Source
VERSION ?= $(REZ_BUILD_PROJECT_VERSION)
ARCHIVE_URL := https://www.libraw.org/data/LibRaw-$(VERSION).tar.gz
LOCAL_ARCHIVE := $(BUILD_ROOT)/LibRaw.$(VERSION).tar.gz

# Build time locations
BUILD_TYPE = Release
BUILD_DIR = ${REZ_BUILD_PATH}/BUILD/$(BUILD_TYPE)
SOURCE_DIR := $(BUILD_DIR)/LibRaw-$(VERSION)/

# Installation prefix
PREFIX ?= ${REZ_BUILD_INSTALL_PATH}

JPEG_ROOT ?= $(REZ_JPEGTURBO_ROOT)

.PHONY: build install test clean
.DEFAULT_GOAL := build

clean:
	rm -rf $(BUILD_ROOT)

$(BUILD_DIR): # Prepare build directories
	mkdir -p $(BUILD_ROOT)
	mkdir -p $(BUILD_DIR)

$(LOCAL_ARCHIVE): | $(BUILD_DIR)
	cd $(BUILD_ROOT) && wget -O $(LOCAL_ARCHIVE) $(ARCHIVE_URL)

$(SOURCE_DIR): $(LOCAL_ARCHIVE)
	cd $(BUILD_DIR) && tar -xvzf $<

build: $(SOURCE_DIR) # configure and build
ifeq "$(VERSION)" "NOT_SET"
	$(warn "No version was specified, provide one with: VERSION=0.20.2")
else
	cd $(SOURCE_DIR) \
	&& autoreconf -f -i \
	&& CPPFLAGS="-I$(JPEG_ROOT)/include" LDFLAGS="-L$(JPEG_ROOT)/lib64" \
	./configure --prefix=$(PREFIX) && make
endif

install: build
	mkdir -p $(PREFIX)
	cd $(SOURCE_DIR) && make install

test: build # Run the tests in the build
	$(MAKE) -C $(BUILD_DIR) test
