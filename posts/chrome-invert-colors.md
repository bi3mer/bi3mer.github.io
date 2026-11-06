+++
date = '2020-05-28T18:22:50-05:00'
draft = false
title = 'Chrome Invert Colors'
+++
If it were up to me, every website would be required to have a theme option of light or dark. Unfortunately, it is not. It is uncommon to find websites that include both options or, at least, default to dark mode. Recently FaceBook included a dark mode option and slack now has it built into their app. It is a wonderful thing to see it become more popular. Still, there is no guarantee. As a result, I have turned to [Dark Reader](https://darkreader.org/). A great chrome extension that will automatically run on all websites but gives you the option to turn off it completely or turn off for certain websites.

It is not a perfect solution, though. On some websites, it won’t work as expected and you are stuck going through the website in a light version; a very jarring experience when coming from a dark screen. As a result, I used a chrome extension that inverted colors. The problem with the extension was twofold. First, it didn’t work on local pdfs. Second, I didn’t know who the developer was and if I could trust them. Because of this, I built my own chrome extension and put it on [GitHub](https://github.com/bi3mer/invertColorsChromeExtension#invertcolorschromeextension).

Before looking at building a chrome extension, we need to be able to invert chrome colors. Luckily, someone has already done the work. A quick search and there was an answer on [StackOverflow(https://stackoverflow.com/questions/4766201/javascript-invert-color-on-all-elements-of-a-page/16239245#16239245)]. No work needed. All I did was open a webpage and run it in the console to make sure it worked.

With this, we can build the extension. At the minimum, an extension needs a manifest.json file and some javascript file that the manifest can call. The manifest file is the following:

```json
{
    "manifest_version": 2,
    "name": "invert",
    "version": "2020.04.29",
    "description": "Invert screen colors.",
    "browser_action": {},
    "background": {
        "scripts": ["background.js"],
        "persistent": false
    },
    "permissions": [
        "http://*/",
        "https://*/"
    ]
}
```

As you can see, we need to give a `manifest_version`, for some reason it had to be greater than one. The name can be anything; I chose invert. The version was the date I made it and the description should likely be more descriptive if you plan on publishing. I gave it no browser action. In the background I have it call the script background.js and note that the call is not persistent. This is where we could be malicious and, for example, set persistent to true and log the user’s keystrokes. Finally, we have the permissions that the extension asks for. In this case, we start by only asking for permission to modify webpages. We’ll come back to this later.

The next question you are probably asking is: what is background.js?

```js
chrome.browserAction.onClicked.addListener(function(tab) {
  chrome.tabs.executeScript(null, {file: "invert.js"});
});
```

If we use invert.js—which contains the inversion code from StackOverflow—instead of background.js then the webpage will not be modified. If we place the inversion code in the callback function and do not call `chrome.tabs.executeScript(...)` then the webpage will also not be modified. The function of background.js is to call the file that inverts the webpage and that is it. Likely there is another way to use chrome.tabs such that two files are not necessary but I did not find it.

We have three files: manifest.json, invert.js, and background.js which form the entire chrome extension. To build the extension, follow these steps:

1. Go to `chrome://extensions/` in your chrome browser.
2. In the top right there is a developer switch. Switch it to on.
3. Click the button in the top left titled “load unpacked”.
4. Select the folder which contains these three files.

You now will have a new extension that will be a small block with the letter “i” in it. By modifying the manifest.json you can include your own image as the icon if you like. When you click the new button the page will invert. If you open a local pdf, the page will not invert. This is because we did not give it permissions for local files, only websites. Modify the manifest.json permissions to include "file://*" in the JSON array. If you click on the invert button again you will see that the change has not yet been registered. Go back to the chrome extension page and click the refresh arrow under the invert extension. The invert on the local pdf will now work.