---
description: >-
  How to connect to MegaBuild.de – on Java Edition, Bedrock, console or mobile.
icon: plug
---

# Connecting to MegaBuild.de

MegaBuild.de supports **crossplay**: Java and Bedrock players play together on the same server.

{% hint style="warning" %}
The server is currently in **maintenance mode**. If you try to connect, you will see a maintenance message instead of the server list. That is not a problem on your end – check [status.megabuild.de](https://status.megabuild.de/) and [Discord](https://megabuild.de/dc/) for updates.
{% endhint %}

## Server address

<table><thead><tr><th width="220">Edition</th><th>Address</th><th width="140">Port</th></tr></thead><tbody><tr><td>Java Edition</td><td><code>megabuild.de</code></td><td>Default (25565)</td></tr><tr><td>Bedrock Edition</td><td><code>megabuild.de</code></td><td><code>19132</code></td></tr></tbody></table>

On Java Edition you do **not** need to enter a port – the default is used automatically.

## Step by step

{% tabs %}
{% tab title="Java Edition" %}
{% stepper %}
{% step %}
#### Launch Minecraft

Start Minecraft Java Edition on the latest compatible version. The currently supported version is announced on [Discord](https://megabuild.de/dc/).
{% endstep %}

{% step %}
#### Open multiplayer

From the main menu, click **Multiplayer**, then **Add Server**.
{% endstep %}

{% step %}
#### Enter the server details

* **Server Name:** MegaBuild.de (anything you like)
* **Server Address:** `megabuild.de`

Confirm with **Done**.
{% endstep %}

{% step %}
#### Join

Select MegaBuild.de from the list and click **Join Server**, or simply double-click the entry.
{% endstep %}
{% endstepper %}
{% endtab %}

{% tab title="Bedrock Edition" %}
Bedrock covers mobile, tablet, Windows, consoles and Nintendo Switch.

{% stepper %}
{% step %}
#### Open the Servers tab

From the main menu go to **Play**, then the **Servers** tab.
{% endstep %}

{% step %}
#### Add a server

Scroll to the bottom and choose **Add Server**.
{% endstep %}

{% step %}
#### Enter the details

* **Server Name:** MegaBuild.de (anything you like)
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
**Console players:** Adding custom servers is restricted on PlayStation, Xbox and Switch depending on the platform. In that case you will need one of the common third-party workarounds (such as a DNS service) to reach external servers.
{% endhint %}
{% endtab %}
{% endtabs %}

## Using Java and Bedrock together

If you play on both a Java and a Bedrock account, you can link them into **one shared save**.

{% content-ref url="connect-account.md" %}
[connect-account.md](connect-account.md)
{% endcontent-ref %}

## It's not working – what now?

<details>

<summary>"Connection failed" or "Can't reach server"</summary>

1. Check [status.megabuild.de](https://status.megabuild.de/) to see whether the server is running or under maintenance.
2. Check the address for typos: `megabuild.de` – no `www.` and no `https://`.
3. On Bedrock: is port `19132` set?

</details>

<details>

<summary>"Outdated client" or "Outdated server"</summary>

Your Minecraft version does not match the server version. Switch to the currently supported version in your launcher – it is announced on [Discord](https://megabuild.de/dc/).

</details>

<details>

<summary>I still can't get in</summary>

Contact [ticket support](https://megabuild.de/ticket/) or ask on [Discord](https://megabuild.de/dc/). Please include:

* Java or Bedrock?
* Which version?
* The exact error message (a screenshot helps)

</details>
