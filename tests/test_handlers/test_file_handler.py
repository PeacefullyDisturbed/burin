"""
Burin File Handler Tests

Copyright (c) 2025 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# Testing values
testFilename = "test.log"


class TestFileHandler:
    """
    Tests the file handler class.
    """

    def test_file_created(self, basic_file_handler, tmp_path):
        """
        Tests that the file is created properly.
        """

        testDir = tmp_path / "fh_test_create"
        filePath = testDir / testFilename
        testDir.mkdir()

        assert filePath.exists() is False

        basic_file_handler(filePath)

        # The file should be created when the handler is created
        assert filePath.exists() is True

    def test_file_created_delay(self, basic_file_handler, basic_record,
                                tmp_path):
        """
        Tests that the file is created when a log is emitted if delay is used.
        """

        testDir = tmp_path / "fh_test_create_delay"
        filePath = testDir / testFilename
        testDir.mkdir()
        createHandler = basic_file_handler(filePath, delay=True)

        # The file should not exist yet since delay was used
        assert filePath.exists() is False

        createRecord = basic_record()
        createHandler.emit(createRecord)

        assert filePath.exists() is True

    def test_emit(self, basic_file_handler, basic_record, tmp_path):
        """
        Tests emitting to a log file.
        """

        testDir = tmp_path / "fh_test_emit"
        filePath = testDir / testFilename
        testDir.mkdir()

        # Use write instead of append mode to ensure file is truncated
        emitHandler = basic_file_handler(filePath, mode="w")
        emitRecord = basic_record()
        emitHandler.emit(emitRecord)

        expectedContents = emitRecord.get_message() + "\n"

        with open(filePath, "r") as logFile:
            assert logFile.read() == expectedContents

    def test_append_emit(self, basic_file_handler, basic_record, tmp_path):
        """
        Tests emitting to a file using the append file mode.
        """

        testDir = tmp_path / "fh_test_append"
        filePath = testDir / testFilename
        testDir.mkdir()
        testText = "Append test\n"

        with open(filePath, "x") as logFile:
            logFile.write(testText)

        appendHandler = basic_file_handler(filePath)
        appendRecord = basic_record()
        appendHandler.emit(appendRecord)

        expectedContents = testText + appendRecord.get_message() + "\n"

        with open(filePath, "r") as appendedFile:
            assert appendedFile.read() == expectedContents

    def test_close(self, basic_file_handler, tmp_path):
        """
        Tests that the handler is closed as expected.
        """

        testDir = tmp_path / "fh_test_close"
        filePath = testDir / testFilename
        testDir.mkdir()
        closeHandler = basic_file_handler(filePath)
        closeHandler.close()

        assert closeHandler.stream is None
        assert closeHandler._closed is True

    def test_repr(self, basic_file_handler, tmp_path):
        """
        Tests that the handler class representation string is correct.
        """

        testDir = tmp_path / "fh_test_repr"
        filePath = testDir / testFilename
        reprHandler = basic_file_handler(filePath, delay=True)

        assert repr(reprHandler) == f"<BurinFileHandler {filePath} (NOTSET)>"
