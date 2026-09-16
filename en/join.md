---
description: >-
  How to connect to MegaBuild.de – whether on Java Edition, Bedrock, console or
  mobile.
icon: plug
---

# Connecting to MegaBuild.de

MegaBuild.de supports **crossplay**: Java and Bedrock players play together on the same server.

{% hint style="warning" %}
The server is currently in **maintenance mode**. If you try to connect, you'll see a maintenance message instead of the server list. That's not a problem on your end – for current info, see [status.megabuild.de](https://status.megabuild.de/) and our [Discord](https://megabuild.de/dc/).
{% endhint %}

## Server address

<table><thead><tr><th width="220">Edition</th><th>Address</th><th width="120">Port</th></tr></thead><tbody><tr><td>Java Edition</td><td><code>megabuild.de</code></td><td>Default (25565)</td></tr><tr><td>Bedrock Edition</td><td><code>megabuild.de</code></td><td><code>19132</code></td></tr></tbody></table>

On Java Edition you **don't need to enter a port** – the default port is used automatically.

## Guide

{% tabs %}
{% tab title="Java Edition" %}
{% stepper %}
{% step %}
#### Start Minecraft

Launch Minecraft Java Edition in the latest compatible version. You can find out which version is currently supported on our [Discord](https://megabuild.de/dc/).
{% endstep %}

{% step %}
#### Go to the Multiplayer menu

In the main menu, click **Multiplayer** and then **Add Server**.
{% endstep %}

{% step %}
#### Enter the server

* **Server Name:** MegaBuild.de (your choice)
* **Server Address:** `megabuild.de`

Confirm with **Done**.
{% endstep %}

{% step %}
#### Join

Select MegaBuild.de in the list and click **Join Server** – or double-click the entry.
{% endstep %}
{% endstepper %}
{% endtab %}

{% tab title="Bedrock Edition" %}
Bedrock covers mobile, tablet, Windows, consoles and the Nintendo Switch.

{% stepper %}
{% step %}
#### Go to the Servers tab

In the main menu, go to **Play** and then to the **Servers** tab.
{% endstep %}

{% step %}
#### Add a server

Scroll all the way down and select **Add Server**.
{% endstep %}

{% step %}
#### Enter the details

* **Server Name:** MegaBuild.de (your choice)
* **Server Address:** `megabuild.de`
* **Port:** `19132`

Save the entry.
{% endstep %}

{% step %}
#### Join

Select MegaBuild.de under your servers and join.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
**Console players:** On PlayStation, Xbox and Switch, adding your own servers is restricted depending on the platform. In that case you need one of the usual third-party solutions (e.g. a DNS service) to reach external servers.
{% endhint %}
{% endtab %}
{% endtabs %}

## Resource pack

On Java Edition you get a **resource pack** when you join, with MegaBuild.de's icons, menus and models.

{% hint style="warning" %}
**The resource pack is required.** If you decline it or the download fails, you'll be disconnected from the server. Accept it the next time you join.

Declined it by accident? Edit the server in your server list and set **Server Resource Packs** to **Enabled**.
{% endhint %}

Bedrock players don't need to do anything – they get the content automatically.

## Using Java and Bedrock together

If you play with both a Java and a Bedrock account, you can link them into **one shared save**.

{% content-ref url="connect-account.md" %}
[connect-account.md](connect-account.md)
{% endcontent-ref %}

## It doesn't work – what now?

<details>

<summary>"Connection failed" or "Server unreachable"</summary>

1. Check [status.megabuild.de](https://status.megabuild.de/) to see whether the server is running or in maintenance.
2. Check the address for typos: `megabuild.de` – without `www.` and without `https://`.
3. On Bedrock: did you enter port `19132`?

</details>

<details>

<summary>"Outdated client" or "Outdated server"</summary>

Your Minecraft version doesn't match the server version. Select the currently supported version in your launcher – you'll find which one that is on our [Discord](https://megabuild.de/dc/).

</details>

<details>

<summary>I still can't get in</summary>

Contact [ticket support](https://megabuild.de/ticket/) or ask on our [Discord](https://megabuild.de/dc/). Describe as precisely as possible:

* Java or Bedrock?
* Which version?
* Which error message appears (a screenshot helps)?

</details>
