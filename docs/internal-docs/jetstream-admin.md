# Administering Jetstream2 for OFO development / advanced Jetstream2

## Updating the `ofo-dev` image

Follow these steps to create and configure a new instance image to serve as a template for OFO team members to create their own development instances.

1. Go to [Exosphere](https://jetstream2.exosphere.app/exosphere/) and select our project/allocation (BIO220124).
3. Click **Create** -> **Instance** in the top right.
4. Click the button for **Ubuntu 24.04**.
5. For **Name**, enter `ofo-dev-YYYYMMDD`, inserting the current date in place of `YYYYMMDD`.
6. For **Flavor**, select **m3.small**.
7. For **Choose a root disk size**, select **Custom** and enter `50` (GB).
8. For **Enable web desktop**, select **No**. (It can still be enabled, if desired, when creating new instances from this instance's image.)
9. For **Choose an SSH public key**, select your key (must have been added during your [JS2 setup](jetstream.md)). Note: your key will be on the ofo-dev VM image and all machines others create from it. This should be OK because anyone in our allocation can access the VM anyway, but if you want to avoid this, you could probably select **None** for SSH key and just connect via SSH using the exouser password provided on the instance's page in Exosphere.
10. Click **Create**.
11. Pull up the instance's page by clicking on the **Instances** box and then clicking on the instance name. Wait for the status in the top right to change to **Ready** in green (approx. 1 minute).
13. Apply the OFO dev Ansible configuration as described in the README of the [ofo-ansible repo](https://github.com/open-forest-observatory/ofo-ansible).
14. Reboot the instance (via command line or Exosphere).
15. On the instance's Exosphere page, click **Actions** -> **Image** and then **Create** (accepting the default name).
16. On the instance's Exosphere page, delete the instance.
