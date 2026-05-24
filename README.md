# Overlayer Testnet Tools 🚀

This collection of Python scripts empowers you to interact seamlessly with the Overlayer testnet, a blockchain test network for decentralized applications. The core script, `main.py`, offers automation and multi-account support for core testnet activities.

🔗 Network: [Overlayer Testnet](https://testnet.overlayer.fi/)

## ✨ Features Overview

### General Features

- **Multi-Account Support**: Reads private keys from `pvkey.txt` to perform actions across multiple accounts.
- **Colorful CLI**: Uses `colorama` for visually appealing output with colored text and borders.
- **Asynchronous Execution**: Built with `asyncio` for efficient blockchain interactions.
- **Error Handling**: Comprehensive error catching for blockchain transactions and RPC issues.
- **Bilingual Support**: Supports both English and Vietnamese output based on user selection.
- **Proxy Support**: Supports HTTP, HTTPS, and SOCKS5 proxies for network requests.
- **Multi-threading**: Concurrent processing of multiple wallets for faster execution.

### Included Scripts

#### 1. Auto Faucet (faucet.py)
- ✅ Auto claim USDT and USDC testnet tokens
- ✅ Check token balances before claiming
- ✅ Retry logic with configurable attempts
- ✅ Transaction confirmation with explorer links

#### 2. Auto Mint (mint.py)
- ✅ Auto mint T+ tokens from USDT
- ✅ Auto mint C+ tokens from USDC
- ✅ Automatic token approval
- ✅ Check balances and allowances
- ✅ Retry logic with gas estimation

#### 3. Auto Stake (stake.py)
- ✅ Auto stake T+ tokens to sT+
- ✅ Auto stake C+ tokens to sC+
- ✅ Automatic token approval
- ✅ Check staking balances
- ✅ Retry logic with gas estimation

#### 4. Auto Redeem (redeem.py)
- ✅ Auto unstake sT+ back to T+
- ✅ Auto unstake sC+ back to C+
- ✅ Auto unwrap T+ back to USDT
- ✅ Auto unwrap C+ back to USDC
- ✅ Automatic token approval
- ✅ Retry logic with gas estimation

#### 5. Auto Bridge (bridge.py)
- ✅ Auto bridge tokens from Ethereum Sepolia to Base Sepolia
- ✅ Uses LayerZero OFT for cross-chain messaging
- ✅ Automatic token approval
- ✅ Check bridge balances
- ✅ Retry logic with gas estimation

#### 6. Auto Bridge Back (bridge_back.py)
- ✅ Auto bridge tokens from Base Sepolia back to Ethereum Sepolia
- ✅ Uses LayerZero OFT for cross-chain messaging
- ✅ Automatic token approval
- ✅ Check bridge balances
- ✅ Retry logic with gas estimation

#### 7. Auto Send (send.py)
- ✅ Auto send ETH to random addresses
- ✅ Auto send ETH to addresses from file (address.txt)
- ✅ Check ETH balance before sending
- ✅ Configurable transaction count and amount
- ✅ Retry logic with gas estimation

#### 8. Auto Receive (receive.py)
- ✅ Auto check ETH balance for multiple wallets
- ✅ Display balance summary
- ✅ Proxy support for balance checking

#### 9. Auto Swap (swap.py)
- ✅ Simulate token swap interactions (USDT to USDC, T+ to C+)
- ✅ Check token balances
- ✅ Display swap simulation results

#### 10. Auto Liquidity (liquidity.py)
- ✅ Simulate adding liquidity for T+/C+ pairs
- ✅ Simulate removing liquidity
- ✅ Check token balances
- ✅ Display liquidity simulation results

#### 11. Auto Mint WL NFT (mintwlnft.py)
- ✅ Auto mint WL NFT via API
- ✅ Check social verification status
- ✅ Sign message with private key
- ✅ Display minted token ID and transaction hash

## 🛠️ Prerequisites

Before running the scripts, ensure you have the following installed:

- Python 3.8+
- `pip` (Python package manager)
- **Dependencies**: Install via `pip install -r requirements.txt` (ensure `web3.py`, `colorama`, `asyncio`, `eth-account`, `aiohttp_socks` and `inquirer` are included).
- **pvkey.txt**: Add private keys (one per line) for wallet automation.
- **proxies.txt** (optional): Add proxy addresses for network requests, if needed.

## 📦 Installation

1. **Clone this repository:**
   ```sh
   git clone https://github.com/thog9/Overlayer-testnet.git
   cd Overlayer-testnet
   ```

2. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Prepare Input Files:**
   - Open the `pvkey.txt`: Add your private keys (one per line) in the root directory.
   ```sh
   nano pvkey.txt
   ```
   Example format:
   ```
   0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
   0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890
   ```

   - Create `proxies.txt` for specific operations (optional):
   ```sh
   nano proxies.txt
   ```
   Example format:
   ```
   http://username:password@proxy.com:8080
   socks5://username:password@proxy.com:1080
   http://proxy.com:8080
   ```

   - Create `address.txt` for send operations (optional):
   ```sh
   nano address.txt
   ```
   Example format:
   ```
   0x1234567890abcdef1234567890abcdef12345678
   0xabcdef1234567890abcdef1234567890abcdef12
   ```

4. **Run:**
   ```sh
   python main.py
   ```
   - Choose a language (Vietnamese/English).
   - Select the desired tool from the menu.

## 📨 Contact

Connect with us for support or updates:

- **Telegram**: [thog099](https://t.me/thog099)
- **Channel**: [CHANNEL](https://t.me/thogairdrops)
- **Group**: [GROUP CHAT](https://t.me/thogchats)
- **X**: [Thog](https://x.com/thog099) 

----

## ☕ Support Us

Love these scripts? Fuel our work with a coffee!

🔗 BUYMECAFE: [BUY ME CAFE](https://buymecafe.vercel.app/)

🔗 WEBSITE: [BUY SCRIPS](https://thogtoolhub.com/)
