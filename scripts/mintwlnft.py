import os
import sys
import asyncio
import aiohttp
import random
from typing import List, Optional, Tuple
from web3 import Web3
from eth_account import Account
from aiohttp_socks import ProxyConnector
from colorama import init, Fore, Style

init(autoreset=True)

BORDER_WIDTH = 80
NETWORK_URL  = "https://ethereum-sepolia-rpc.publicnode.com"
CHAIN_ID     = 11155111
EXPLORER_URL = "https://sepolia.etherscan.io/tx/0x"
API_BASE_URL = "https://api.overlayer.fi"

CONFIG = {
    "THREADS":        5,
    "RETRY_ATTEMPTS": 3,
    "RETRY_DELAY":    5,
    "TIMEOUT":        60,
    "DELAY_BETWEEN":  3,
    "TASK_DELAY":     2,
}

OG_NFT_CONTRACT = Web3.to_checksum_address("0x25426bBB816aB8dAA4F9ED60ACc31Fc14fc199aa")

ERC721_ABI = [
    {"inputs": [{"name": "owner", "type": "address"}],
     "name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}],
     "stateMutability": "view", "type": "function"},
    {"inputs": [{"name": "tokenId", "type": "uint256"}],
     "name": "tokenURI", "outputs": [{"name": "", "type": "string"}],
     "stateMutability": "view", "type": "function"},
    {"inputs": [{"name": "owner", "type": "address"}],
     "name": "tokensOfOwner", "outputs": [{"name": "", "type": "uint256[]"}],
     "stateMutability": "view", "type": "function"},
]

MINT_ABI = [
    {"inputs": [{"internalType": "uint256", "name": "nonce", "type": "uint256"},
                {"internalType": "bytes",   "name": "signature", "type": "bytes"}],
     "name": "mint", "outputs": [{"name": "tokenId", "type": "uint256"}],
     "stateMutability": "nonpayable", "type": "function"},
]

LANG = {
    'vi': {
        'title':             'OVERLAYER - AUTO MINT WL NFT',
        'found_wallets':     'Tìm thấy {count} ví trong pvkey.txt',
        'found_proxies':     'Tìm thấy {count} proxy',
        'no_proxies':        'Không có proxy, chạy trực tiếp',
        'processing':        '⚙ ĐANG XỬ LÝ {count} VÍ',
        'pausing':           'Tạm dừng',
        'completed':         '✅ HOÀN THÀNH: {ok}/{total} VÍ MINT NFT THÀNH CÔNG',
        'pvkey_not_found':   '❌ Không tìm thấy pvkey.txt',
        'pvkey_empty':       '❌ Không có private key hợp lệ',
        'invalid_key':       'Dòng {i}: không hợp lệ, bỏ qua',
        'no_proxy':          'Không có proxy',
        'unknown_ip':        'Không xác định',
        'proxy_line':        '🔄 Proxy: [{proxy}] | IP: [{ip}]',
        'wallet_label':      'Ví',
        'retry':             'Retry {cur}/{max}...',
        'max_retry':         'Hết số lần thử',
        'connect_ok':        'Kết nối Ethereum Sepolia thành công!',
        'connect_fail':      'Không thể kết nối RPC',
        'checking_balance':  'Đang kiểm tra số dư NFT...',
        'balance_info':      '- NFT Balance: {nft}',
        'getting_nonce':     'Đang lấy nonce từ API...',
        'nonce_fail':        'Không thể lấy nonce',
        'minting':           'Đang mint NFT...',
        'mint_ok':           'Mint NFT thành công! Tx: {tx}',
        'mint_fail':         'Mint NFT thất bại',
        'insufficient_eth':  'Số dư ETH không đủ cho gas',
        'summary_header':    '📊 Tóm tắt:',
        'summary_wallet':    '- Wallet:      {v}',
        'summary_nft':       '- NFT Balance: {v}',
        'success_line':      '✅ Thành công | Ví: {addr} | NFT: {nft}',
        'err_runtime':       'Lỗi: {e}',
    },
    'en': {
        'title':             'OVERLAYER - AUTO MINT WL NFT',
        'found_wallets':     'Found {count} wallets in pvkey.txt',
        'found_proxies':     'Found {count} proxies',
        'no_proxies':        'No proxies, running direct',
        'processing':        '⚙ PROCESSING {count} WALLETS',
        'pausing':           'Pausing',
        'completed':         '✅ COMPLETED: {ok}/{total} WALLETS MINT NFT SUCCESS',
        'pvkey_not_found':   '❌ pvkey.txt not found',
        'pvkey_empty':       '❌ No valid private keys',
        'invalid_key':       'Line {i}: invalid key, skipped',
        'no_proxy':          'No proxy',
        'unknown_ip':        'Unknown',
        'proxy_line':        '🔄 Proxy: [{proxy}] | IP: [{ip}]',
        'wallet_label':      'Wallet',
        'retry':             'Retry {cur}/{max}...',
        'max_retry':         'Max retries reached',
        'connect_ok':        'Connected to Ethereum Sepolia!',
        'connect_fail':      'Failed to connect to RPC',
        'checking_balance':  'Checking NFT balance...',
        'balance_info':      '- NFT Balance: {nft}',
        'getting_nonce':     'Getting nonce from API...',
        'nonce_fail':        'Failed to get nonce',
        'minting':           'Minting NFT...',
        'mint_ok':           'Mint NFT successful! Tx: {tx}',
        'mint_fail':         'Mint NFT failed',
        'insufficient_eth':  'Insufficient ETH for gas',
        'summary_header':    '📊 Summary:',
        'summary_wallet':    '- Wallet:      {v}',
        'summary_nft':       '- NFT Balance: {v}',
        'success_line':      '✅ Success | Wallet: {addr} | NFT: {nft}',
        'err_runtime':       'Error: {e}',
    },
}

def print_border(text: str, color=Fore.CYAN, width=BORDER_WIDTH):
    text = text.strip()
    if len(text) > width - 4:
        text = text[:width - 7] + "..."
    padded = f" {text} ".center(width - 2)
    print(f"{color}┌{'─' * (width - 2)}┐{Style.RESET_ALL}")
    print(f"{color}│{padded}│{Style.RESET_ALL}")
    print(f"{color}└{'─' * (width - 2)}┘{Style.RESET_ALL}")

def print_separator(color=Fore.MAGENTA):
    print(f"{color}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")

def p(icon: str, text: str, color=Fore.CYAN):
    print(f"{color}  {icon} {text}{Style.RESET_ALL}")

def load_private_keys() -> List[Tuple[int, str]]:
    fp = "pvkey.txt"
    if not os.path.exists(fp):
        p("✖", LANG['pvkey_not_found'], Fore.RED)
        with open(fp, 'w') as f:
            f.write("# Mỗi dòng một private key\n")
        sys.exit(1)
    keys = []
    with open(fp) as f:
        for i, line in enumerate(f, 1):
            k = line.strip()
            if not k or k.startswith('#'):
                continue
            if not k.startswith('0x'):
                k = '0x' + k
            try:
                Account.from_key(k)
                keys.append((i, k))
            except Exception:
                p("⚠", LANG['invalid_key'].format(i=i), Fore.YELLOW)
    if not keys:
        p("✖", LANG['pvkey_empty'], Fore.RED)
        sys.exit(1)
    return keys

def load_proxies() -> List[str]:
    if not os.path.exists("proxies.txt"):
        return []
    return [l.strip() for l in open("proxies.txt") if l.strip() and not l.startswith('#')]

def parse_proxy(proxy: Optional[str]) -> Optional[str]:
    if not proxy:
        return None
    proxy = proxy.strip()
    if proxy.startswith(("http://", "https://", "socks4://", "socks5://")):
        return proxy
    parts = proxy.split(":")
    if len(parts) == 4:
        host, port, user, pwd = parts
        return f"http://{user}:{pwd}@{host}:{port}"
    if len(parts) == 2:
        return f"http://{parts[0]}:{parts[1]}"
    return f"http://{proxy}"

def make_connector(proxy_url: Optional[str]):
    if not proxy_url:
        return aiohttp.TCPConnector(ssl=False)
    if proxy_url.startswith("socks"):
        return ProxyConnector.from_url(proxy_url, ssl=False)
    return aiohttp.TCPConnector(ssl=False)

def proxy_kwargs(proxy_url: Optional[str]) -> dict:
    if not proxy_url or proxy_url.startswith("socks"):
        return {}
    return {"proxy": proxy_url}

async def get_proxy_ip(proxy_url: Optional[str]) -> str:
    try:
        connector = make_connector(proxy_url)
        kw        = proxy_kwargs(proxy_url)
        timeout   = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as s:
            async with s.get("https://api.ipify.org?format=json", **kw) as r:
                data = await r.json()
                return data.get("ip", LANG['unknown_ip'])
    except Exception:
        return LANG['unknown_ip']

def connect_web3(proxy: Optional[str] = None) -> Web3:
    req_kwargs = {"timeout": 30}
    if proxy:
        req_kwargs["proxies"] = {"http": proxy, "https": proxy}
    w3 = Web3(Web3.HTTPProvider(NETWORK_URL, request_kwargs=req_kwargs))
    if w3.is_connected():
        p("✓", LANG['connect_ok'], Fore.GREEN)
        return w3
    p("✖", LANG['connect_fail'], Fore.RED)
    sys.exit(1)

async def wait_for_receipt(w3: Web3, tx_hash: str, max_wait: int = 300):
    start = asyncio.get_event_loop().time()
    while True:
        try:
            receipt = w3.eth.get_transaction_receipt(tx_hash)
            if receipt is not None:
                return receipt
        except Exception:
            pass
        if asyncio.get_event_loop().time() - start > max_wait:
            return None
        await asyncio.sleep(5)

def get_nft_balance(w3: Web3, contract_addr: str, wallet: str) -> int:
    try:
        nft = w3.eth.contract(address=Web3.to_checksum_address(contract_addr), abi=ERC721_ABI)
        balance = nft.functions.balanceOf(wallet).call()
        return balance
    except Exception:
        return 0

async def get_social_info(address: str, proxy_url: Optional[str] = None) -> Optional[dict]:
    try:
        connector = make_connector(proxy_url)
        kw        = proxy_kwargs(proxy_url)
        timeout   = aiohttp.ClientTimeout(total=30)
        url       = f"{API_BASE_URL}/api-s/socials/{address}"
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as s:
            async with s.get(url, **kw) as r:
                if r.status == 200:
                    data = await r.json()
                    return data
        return None
    except Exception:
        return None

def sign_message(private_key: str, message: str) -> str:
    account = Account.from_key(private_key)
    message_hash = Web3.keccak(text=message)
    signature = account.sign_message(message_hash)
    return signature.signature.hex()

async def mint_nft_api(address: str, private_key: str, proxy_url: Optional[str] = None) -> Optional[dict]:
    try:
        connector = make_connector(proxy_url)
        kw        = proxy_kwargs(proxy_url)
        timeout   = aiohttp.ClientTimeout(total=30)
        url       = f"{API_BASE_URL}/api-s/socials/og/mint/{address}"
        
        # Generate timestamp and random string
        timestamp = str(int(asyncio.get_event_loop().time()))
        random_str = Web3.keccak(text=f"{address}{timestamp}").hex()[:32]
        
        # Create message
        message = f"Request Overlayer OG mint\n{address}\n{timestamp}\n{random_str}"
        
        # Sign message
        signature = sign_message(private_key, message)
        
        payload = {
            "message": message,
            "signature": signature
        }
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as s:
            async with s.post(url, json=payload, **kw) as r:
                if r.status == 200:
                    data = await r.json()
                    return data
        return None
    except Exception as e:
        return None

async def process_wallet(index: int, private_key: str, proxy: Optional[str], 
                         w3: Web3) -> Tuple[bool, int]:
    account = Account.from_key(private_key)
    address = account.address
    short = f"{address[:6]}...{address[-4:]}"
    proxy_url = parse_proxy(proxy)
    proxy_str = proxy or LANG['no_proxy']

    print_border(f"{LANG['wallet_label']} {index}: {short}", Fore.YELLOW)
    ip = await get_proxy_ip(proxy_url)
    print(f"{Fore.CYAN}  {LANG['proxy_line'].format(proxy=proxy_str, ip=ip)}{Style.RESET_ALL}")
    print()

    try:
        p(">", LANG['checking_balance'], Fore.CYAN)
        nft_bal = get_nft_balance(w3, OG_NFT_CONTRACT, address)
        print(f"{Fore.WHITE}  {LANG['balance_info'].format(nft=nft_bal)}{Style.RESET_ALL}")
        print()

        label = "── MINT WL NFT ──"
        print(f"{Fore.CYAN}┌─ {label} {'─' * (BORDER_WIDTH - len(label) - 4)}{Style.RESET_ALL}")

        # Check social verification
        print(f"{Fore.CYAN}│{Style.RESET_ALL}  {Fore.CYAN}> Checking social verification...{Style.RESET_ALL}")
        social_info = await get_social_info(address, proxy_url)
        
        if social_info:
            x_verified = social_info.get('x_verified', 'not verified')
            print(f"{Fore.CYAN}│{Style.RESET_ALL}  {Fore.WHITE}  X Verified: {Fore.YELLOW}{x_verified}{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}│{Style.RESET_ALL}  {Fore.YELLOW}  Could not fetch social info{Style.RESET_ALL}")
        
        await asyncio.sleep(random.uniform(1, 2))

        # Mint via API
        print(f"{Fore.CYAN}│{Style.RESET_ALL}  {Fore.CYAN}> {LANG['minting']}{Style.RESET_ALL}")
        mint_result = await mint_nft_api(address, private_key, proxy_url)
        
        if mint_result:
            token_id = mint_result.get('tokenId')
            tx_hash = mint_result.get('txHash')
            tx_link = f"{EXPLORER_URL}{tx_hash}"
            print(f"{Fore.CYAN}│{Style.RESET_ALL}  {Fore.WHITE}  Token ID: {Fore.YELLOW}{token_id}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}│{Style.RESET_ALL}  {Fore.WHITE}  Tx: {Fore.CYAN}{tx_link}{Style.RESET_ALL}")
            p("✓", LANG['mint_ok'].format(tx=tx_link), Fore.GREEN)
            mint_success = True
        else:
            p("✖", LANG['mint_fail'], Fore.RED)
            mint_success = False

        print(f"{Fore.CYAN}└{'─' * (BORDER_WIDTH - 2)}{Style.RESET_ALL}")
        print()

        # Update balance
        nft_bal = get_nft_balance(w3, OG_NFT_CONTRACT, address)

        print(f"{Fore.WHITE}  {'─' * 50}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  {LANG['summary_header']}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}     {LANG['summary_wallet'].format(v=f'{Fore.YELLOW}{short}{Style.RESET_ALL}')}")
        print(f"{Fore.WHITE}     {LANG['summary_nft'].format(v=f'{Fore.CYAN}{nft_bal}{Style.RESET_ALL}')}")
        print(f"{Fore.WHITE}  {'─' * 50}{Style.RESET_ALL}")
        print()

        if mint_success:
            print(f"{Fore.GREEN}  {LANG['success_line'].format(addr=short, nft=nft_bal)}{Style.RESET_ALL}")
            print()
            return True, nft_bal
        else:
            return False, nft_bal

    except Exception as e:
        import traceback
        p("✖", LANG['err_runtime'].format(e=e), Fore.RED)
        print(f"{Fore.RED}{traceback.format_exc()}{Style.RESET_ALL}")
        return False, 0

async def run_mintwlnft(language: str = 'vi'):
    global LANG
    LANG = LANG[language]
    print()
    print_border(LANG['title'], Fore.CYAN)
    print()

    private_keys = load_private_keys()
    p("ℹ", LANG['found_wallets'].format(count=len(private_keys)), Fore.YELLOW)

    proxies = load_proxies()
    if proxies:
        p("ℹ", LANG['found_proxies'].format(count=len(proxies)), Fore.YELLOW)
    else:
        p("ℹ", LANG['no_proxies'], Fore.YELLOW)

    print()
    w3 = connect_web3()
    print()

    print_separator()
    print_border(LANG['processing'].format(count=len(private_keys)), Fore.MAGENTA)
    print()

    total = len(private_keys)
    ok_count = 0
    sema = asyncio.Semaphore(CONFIG['THREADS'])

    async def run_one(i: int, pnum: int, key: str):
        nonlocal ok_count
        proxy = proxies[i % len(proxies)] if proxies else None
        async with sema:
            ok, _ = await process_wallet(pnum, key, proxy, w3)
            if ok:
                ok_count += 1
            if i < total - 1:
                delay = CONFIG['DELAY_BETWEEN']
                p("ℹ", f"{LANG['pausing']} {delay}s...", Fore.YELLOW)
                await asyncio.sleep(delay)

    await asyncio.gather(
        *[run_one(i, pnum, key) for i, (pnum, key) in enumerate(private_keys)],
        return_exceptions=True
    )

    print()
    print_separator()
    print_border(LANG['completed'].format(ok=ok_count, total=total), Fore.GREEN)
    print()

if __name__ == "__main__":
    asyncio.run(run_mintwlnft('vi'))
