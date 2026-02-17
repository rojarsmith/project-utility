#define UNICODE
#define _UNICODE
#include <windows.h>
#include <shellapi.h>

namespace {
constexpr UINT kTrayIconId = 1;
constexpr UINT kTrayMsg = WM_APP + 1;
const wchar_t kClassName[] = L"TrayWinMainWindow";

ATOM RegisterTrayClass(HINSTANCE instance) {
    WNDCLASSEXW wc{};
    wc.cbSize = sizeof(wc);
    wc.lpfnWndProc = [](HWND hwnd, UINT msg, WPARAM wparam, LPARAM lparam) -> LRESULT {
        switch (msg) {
        case WM_DESTROY:
            PostQuitMessage(0);
            return 0;
        case kTrayMsg:
            // Handle tray icon interactions here if needed.
            return 0;
        default:
            return DefWindowProcW(hwnd, msg, wparam, lparam);
        }
    };
    wc.hInstance = instance;
    wc.lpszClassName = kClassName;
    return RegisterClassExW(&wc);
}

HWND CreateTrayWindow(HINSTANCE instance) {
    return CreateWindowExW(
        0,
        kClassName,
        L"Tray Window",
        0,
        0, 0, 0, 0,
        HWND_MESSAGE,
        nullptr,
        instance,
        nullptr);
}

bool AddTrayIcon(HWND hwnd, HINSTANCE instance) {
    NOTIFYICONDATAW nid{};
    nid.cbSize = sizeof(nid);
    nid.hWnd = hwnd;
    nid.uID = kTrayIconId;
    nid.uFlags = NIF_MESSAGE | NIF_ICON | NIF_TIP;
    nid.uCallbackMessage = kTrayMsg;
    nid.hIcon = LoadIconW(nullptr, IDI_APPLICATION);
    lstrcpyW(nid.szTip, L"Tray icon running");

    return Shell_NotifyIconW(NIM_ADD, &nid) == TRUE;
}

void RemoveTrayIcon(HWND hwnd) {
    NOTIFYICONDATAW nid{};
    nid.cbSize = sizeof(nid);
    nid.hWnd = hwnd;
    nid.uID = kTrayIconId;
    Shell_NotifyIconW(NIM_DELETE, &nid);
}
} // namespace

int WINAPI wWinMain(HINSTANCE instance, HINSTANCE, PWSTR, int) {
    if (!RegisterTrayClass(instance)) {
        return 1;
    }

    HWND hwnd = CreateTrayWindow(instance);
    if (!hwnd) {
        return 1;
    }

    if (!AddTrayIcon(hwnd, instance)) {
        return 1;
    }

    MSG msg{};
    while (GetMessageW(&msg, nullptr, 0, 0) > 0) {
        TranslateMessage(&msg);
        DispatchMessageW(&msg);
    }

    RemoveTrayIcon(hwnd);
    return 0;
}

int WINAPI WinMain(HINSTANCE instance, HINSTANCE prev, LPSTR, int show) {
    // Provide ANSI entry point for toolchains that expect WinMain.
    return wWinMain(instance, prev, GetCommandLineW(), show);
}
