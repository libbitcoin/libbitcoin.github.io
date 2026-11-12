# Configuration

## 1. Running bs

The executable is `bs` (`bs.exe` on Windows), and the examples run the
same on Linux, macOS and Windows. `bs` runs with built-in mainnet
defaults. No configuration file is read unless `--config` is given.

Run with defaults. The store is created in a `mainnet` directory under
the current directory if it does not exist.

```
$ bs
```

With a configuration file:

```
$ bs --config bs.cfg
```

To run on testnet3, testnet4, testnet5, regtest or signet, with the store in a
directory named for the network:

```
$ bs -n testnet4
```

Until the chain is current, only the admin site accepts connections. P2P peers, the block explorer and the other client services
wait ([Until current](services#until-current)).

## 2. Pages

| Page | Contents |
| ---- | -------- |
| [Command Line](command-line) | Command line options and the running console. |
| [Configuration File](file) | File syntax, and displaying the settings in effect. |
| [Common Setups](setups) | Sync modes, checkpoints, each service, client filters, silent payments, anonymizing networks, peers and load balancing. |
| [Conventional Ports](ports) | The ports of every service on each chain. |
| [Community Servers](public) | The community servers, and running your own. |
| [Store Settings](store) | Table sizing, bucket autotuning, and the settings fixed when a store is created. |
| [Service Settings](services) | Listening, TLS, authentication, HTTP and limits, shared by every service. |
| [Performance Settings](performance) | Processor, GPU, network and NUMA settings. |
| [Settings Reference](reference) | Every setting, by section, with its description and default. |
| [BX Settings](bx) | The configuration of Bitcoin Explorer (`bx`). |
| [Testnet3](testnet3), [Testnet4](testnet4), [Testnet5](testnet5), [Signet](signet), [Regtest](regtest) | Settings for the test chains. |
