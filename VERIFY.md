# Verifying the files

Three independent levels. Level 1 is enough to detect corruption; levels 2–3 prove the files come from
the author.

Signing key: **Vincent Liu &lt;elsevier2012@hotmail.com&gt;**
Fingerprint: `DA1A 1AEF D8B2 C17C FF3F 1D1B 3905 0F50 7A4F EC17`
The same fingerprint is published in the Zenodo record [10.5281/zenodo.23564899](https://doi.org/10.5281/zenodo.23564899) and on
[GitHub](https://github.com/AlienMuse.gpg) (`https://github.com/AlienMuse.gpg`).

## Level 1 — checksums

Download the PDFs and `SHA256SUMS` into one folder.

Linux / macOS:

```sh
sha256sum -c SHA256SUMS --ignore-missing
```

Windows PowerShell:

```powershell
Get-Content SHA256SUMS | ForEach-Object {
  $hash, $name = $_ -split '  ', 2
  if (Test-Path $name) {
    $ok = (Get-FileHash $name -Algorithm SHA256).Hash -eq $hash.ToUpper()
    "{0}  {1}" -f ($(if ($ok) { 'OK  ' } else { 'FAIL' })), $name
  }
}
```

## Level 2 — signature

```sh
gpg --import VincentLiu-signing-key.asc          # from this repository or the release
gpg --verify SHA256SUMS.asc SHA256SUMS
```

The output must say `Good signature from "Vincent Liu <elsevier2012@hotmail.com>"` and show the fingerprint
above.

## Level 3 — timestamps and platform attestation
GitHub releases of this repository are immutable and carry a GitHub-signed release attestation:

```sh
gh release verify v1.0.0 -R AlienMuse/arithmetic-spectral-descent
gh release verify-asset v1.0.0 Arithmetic-Spectral-Descent-v1.0.0-Complete.pdf -R AlienMuse/arithmetic-spectral-descent
```

`SHA256SUMS.tsr` is an RFC 3161 timestamp token over `SHA256SUMS` from FreeTSA:

```sh
openssl ts -reply -in SHA256SUMS.tsr -text          # shows the time
openssl ts -verify -data SHA256SUMS -in SHA256SUMS.tsr \
    -CAfile timestamps/freetsa-cacert.pem -untrusted timestamps/freetsa-tsa.crt
```

A second, independent token over the same file comes from DigiCert. Its certificate chain up to the public
*DigiCert Trusted Root G4* is in `timestamps/digicert-chain.pem`; verify against your system's CA bundle:

```sh
openssl ts -verify -data SHA256SUMS -in timestamps/SHA256SUMS.digicert.tsr \
    -CAfile /etc/ssl/certs/ca-certificates.crt -untrusted timestamps/digicert-chain.pem
```

`SHA256SUMS.ots` anchors the same file in the Bitcoin blockchain (<https://opentimestamps.org>):

```sh
ots verify SHA256SUMS.ots
```

## Checksums of this release

```text
e7a1f16438f5cd43218d49963e7435a9433c6a811508bbeae7ad34a34d6c2bb6  Arithmetic-Spectral-Descent-v1.0.0-Complete.pdf
128d1feb7f97e5a71bae6c32833ec4bd51aca64a67b47e83cf179236e08c6b14  Arithmetic-Spectral-Descent-v1.0.0-Preview.pdf
464bd80e21694eb2ae1779e1488b12d6d52a166b5c2e17383cbad7e0a68fc915  Arithmetic-Spectral-Descent-v1.0.0-numerics.zip
```
