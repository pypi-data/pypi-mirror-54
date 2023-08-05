# SDK Python

## Requirements

- Python >= 3.X

## Install

```bash
pip install katena-chain-sdk-py
```

## Usage

To rapidly interact with our API, you can use our `Transactor` helper. It handles all the steps needed to correctly
format, sign and send a tx.

Feel free to explore and modify its code to meet your expectations.

## Examples

Detailed examples are provided in the `examples` folder to explain how to use our `Transactor` helper methods.

Available examples:
* Send a `Certificate`
* Retrieve a `Certificate`
* Retrieve a list of historical `Certificate`
* Encrypt and send a `Secret`
* Retrieve a list of `Secret`

For instance, to send a certificate:
```bash
python examples/send_certificate_raw.py
```

## Katena documentation

For more information, check the [katena documentation](https://doc.katena.transchain.io).
