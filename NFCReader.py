from smartcard.scard import *

try:
    hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)
    if hresult != SCARD_S_SUCCESS:
        raise error(
            "Failed to establish context: " + SCardGetErrorMessage(hcontext)
        )
    print('Context Established')

    try:
        hresult, readers = SCardListReaders(hcontext, [])
        if hresult != SCARD_S_SUCCESS:
            raise error(
                "Failed to retrieve readers: " + SCardGetErrorMessage(hresult)
            )
        readerStates = [(readers[0], SCARD_STATE_UNAWARE)]
        hresult, newstates = SCardGetStatusChange(hcontext, 0, readerStates)

        hresult2, newstates = SCardGetStatusChange(hcontext, INFINITE, newstates)
        if newstates[0][1] == SCARD_STATE_PRESENT:
            print('New card detected')

        print(newstates[0][1])

    except error as e:
        print(e)

except error as e:
    print(e)



