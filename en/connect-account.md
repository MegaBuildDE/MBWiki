---
description: >-
  How to link your Java and Bedrock accounts on MegaBuild.de into one shared
  save.
icon: link
---

# Linking Java & Bedrock accounts

MegaBuild.de supports crossplay. If you play on both a **Java** and a **Bedrock** account (mobile, tablet, Windows, console), you can link them into one shared save.

{% hint style="info" %}
If you play **only** Java **or only** Bedrock, you can skip this page.
{% endhint %}

{% hint style="danger" %}
**Read this before linking.**

Linking merges your Bedrock account into the save of your **Java** account. Any existing **progress on the Bedrock account will be lost.**

So link your accounts **before** you seriously start playing on the Bedrock account.
{% endhint %}

## Step by step

{% stepper %}
{% step %}
#### Join with both accounts

Connect to the server with **both** accounts:

```
megabuild.de
```

Bedrock additionally uses port `19132`.

{% content-ref url="join.md" %}
[join.md](join.md)
{% endcontent-ref %}
{% endstep %}

{% step %}
#### Run the command on your Java account

Type this in chat on your **Java** account:

```
/linkaccount <bedrock-account-name>
```
{% endstep %}

{% step %}
#### Enter the code on your Bedrock account

You will receive a code in the chat of your Java account. Enter it on your **Bedrock** account:

```
/linkaccount <java-account-name> <code>
```
{% endstep %}

{% step %}
#### Rejoin

If everything worked, you will be kicked and asked to rejoin. From your next login onwards, both accounts share the same save.
{% endstep %}
{% endstepper %}

## Important notes

{% hint style="warning" %}
**Transferring money to other accounts in order to bypass rules is not allowed** and is treated as a rule violation. The full rules are at [megabuild.de/rules](https://megabuild.de/rules/).
{% endhint %}

<details>

<summary>The command doesn't work</summary>

* Check the spelling of both account names – capitalisation matters.
* Make sure **both** accounts are online at the same time.
* The code is usually only valid for a short time. If it expired, start over.

</details>

<details>

<summary>Can I unlink the accounts again?</summary>

Contact [ticket support](https://megabuild.de/ticket/). Note that unlinking does not automatically restore the merged save.

</details>

<details>

<summary>I linked the wrong account</summary>

Contact [ticket support](https://megabuild.de/ticket/) as soon as possible – the sooner, the better the chances of fixing it cleanly.

</details>

## More help

{% content-ref url="support.md" %}
[support.md](support.md)
{% endcontent-ref %}
