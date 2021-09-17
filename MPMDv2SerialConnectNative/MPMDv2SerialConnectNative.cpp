#include <windows.h>
#include <tchar.h>
#include <atlstr.h>
#include <comdef.h>

#define PORT_NAME _T("\\\\.\\COM8")
#define READ_BUFFER_LENGTH 1024

void printline(LPCTSTR pszFormat, ...) {
    va_list _ArgList;
    va_start(_ArgList, pszFormat);
    _vtprintf(pszFormat, _ArgList);
    va_end(_ArgList);
    _tprintf(_T("\r\n"));
}

void printConsole(char* pszText) {
    USES_CONVERSION;
    LPCTSTR cszText = A2T(pszText);
    if (cszText == NULL) return;
    _tprintf(cszText);
}

void printLastError() {
    DWORD lastError = GetLastError();
    DWORD hr = HRESULT_FROM_WIN32(lastError);
    _com_error err(hr);
    printline(_T("ERROR 0x%08X \"%s\""), hr, err.ErrorMessage());
}

int mainNonOverlapped() {
    printline(_T("Opening %s 115200 N 8 1 to read"), PORT_NAME);
    HANDLE hComPort = CreateFile(
        PORT_NAME,
        GENERIC_READ | GENERIC_WRITE,
        0, // exclusive access
        NULL, // no security
        OPEN_EXISTING,
        0,
        NULL);
    if (hComPort == INVALID_HANDLE_VALUE) {
        printline(_T("ERROR w/ CreateFile"));
        goto error;
    }

    DCB dcb;
    SecureZeroMemory(&dcb, sizeof(DCB));
    dcb.DCBlength = sizeof(DCB);
    if (!GetCommState(hComPort, &dcb)) {
        printline(_T("ERROR w/ GetCommState"));
        goto error;
    }
    dcb.BaudRate = CBR_115200;
    dcb.Parity = NOPARITY;
    dcb.ByteSize = 8;
    dcb.StopBits = ONESTOPBIT;
    if (!SetCommState(hComPort, &dcb)) {
        printline(_T("ERROR w/ SetCommState"));
        goto error;
    }

    printline(_T("Reading..."));
    char szReadBuffer[READ_BUFFER_LENGTH + 1];
    DWORD dwCharsRead;
    while (TRUE) {
        if (!ReadFile(hComPort, szReadBuffer, READ_BUFFER_LENGTH, &dwCharsRead, NULL)) {
            printline(_T("ERROR w/ ReadFile"));
            goto error;
        }
        if (dwCharsRead > 0) {
            szReadBuffer[dwCharsRead] = NULL;
            printConsole(szReadBuffer);
        }
    };

    return 0;

error:
    printLastError();
    if (hComPort != INVALID_HANDLE_VALUE) {
        CloseHandle(hComPort);
        hComPort = INVALID_HANDLE_VALUE;
    }
    return 1;
}

int mainOverlapped() {
    // TODO:(pv) Overlapped IO version similar to how pyserial is implemented
    //  https://github.com/pyserial/pyserial/blob/master/serial/serialwin32.py
    //...
    return 1;
}

int _tmain(int argc, TCHAR* argv[]) {
    return mainNonOverlapped();
}
