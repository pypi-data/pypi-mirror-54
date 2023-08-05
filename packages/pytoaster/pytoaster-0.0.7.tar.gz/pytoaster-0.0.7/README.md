<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/zhunhung/toaster">
    <img src="https://raw.githubusercontent.com/zhunhung/toaster/master/images/toaster_image.jpg" alt="Logo" width="180" height="180">
  </a>

  <h3 align="center">Toaster</h3>

  <p align="center">
    A simple python library that sends you a message on your preferred channel when your code finished running or encountered an error.
    <br />
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents


* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Frequently Asked Questions](#frequently-asked-questions)
* [Contributing](#contributing)
* [License](#license)
* [Acknowledgements](#acknowledgements)


<!-- GETTING STARTED -->
## Getting Started

To set up Toaster, simply follow the installation and usage example.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Preferred notification channel (Telegram account/Slack Webhook URL)
* Python 3

### Installation

1. Install via pip
```sh
pip install pytoaster
```

<!-- USAGE EXAMPLES -->
## Usage

#### Step 1. Import methods and configure toaster using `set_config()`.
```python
from toaster import telegram_toast, slack_toast, set_config

# for telegram notification
set_config(config_str=<your_telegram_id>, notification_channel='telegram')

# for slack notification
set_config(config_str=<incoming_webhook>, notification_channel='slack')
```  
*Note*: You'll only have to do this once, it'll then be saved to `config.json` in toaster's installation path.

#### Step 2. Add `@(channeltype)_toast` above functions that you want to be notified upon completion.
```python
# telegram example
@telegram_toast
def test_func(a,b):
    time.sleep(5)
    return 'Return {} and {}'.format(str(a),str(b))

# slack example
@slack_toast
def test_func(a,b):
    time.sleep(5)
    return 'Return {} and {}'.format(str(a),str(b))
```

#### Step 3. You'll be notified by according to your preferred channel when your code finishes executing.  
##### - Telegram Example: Notification by [@FreshToasterBot](http://t.me/freshtoasterbot)
<img src="https://raw.githubusercontent.com/zhunhung/toaster/master/images/sample_response.jpg" alt="Telegram Sample Response" width="380" height="100">

##### - Slack Example:
<img src="https://raw.githubusercontent.com/zhunhung/toaster/master/images/slack_sample_response.jpg" alt="Slack Sample Response" width="380" height="100">

<!-- FAQ -->
## Frequently Asked Questions

#### 1. How do I find my Telegram ID?  
Get your telegram ID from [@FreshToasterBot](http://t.me/freshtoasterbot) on Telegram  
<img src="https://raw.githubusercontent.com/zhunhung/toaster/master/images/start_convo.jpg" alt="Start Convo" width="350" height="100">  

#### 2. How do I setup my Slack Webhook?  
Follow the [official instructions](https://slack.com/intl/en-sg/help/articles/115005265063-incoming-webhooks-for-slack) from Slack  
<img src="https://raw.githubusercontent.com/zhunhung/toaster/master/images/webhook_setup.jpg" alt="Slack Instructions" width="350" height="200">


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* Gal Shir for his cute toaster design [https://galshir.com/](https://galshir.com/)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/zhunhung/toaster.svg?style=flat-square
[contributors-url]: https://github.com/zhunhung/toaster/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/zhunhung/toaster.svg?style=flat-square
[forks-url]: https://github.com/zhunhung/toaster/network/members
[stars-shield]: https://img.shields.io/github/stars/zhunhung/toaster.svg?style=flat-square
[stars-url]: https://github.com/zhunhung/toaster/stargazers
[issues-shield]: https://img.shields.io/github/issues/zhunhung/toaster.svg?style=flat-square
[issues-url]: https://github.com/zhunhung/toaster/issues
[license-shield]: https://img.shields.io/github/license/zhunhung/toaster.svg?style=flat-square
[license-url]: https://github.com/zhunhung/toaster/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/zhunhung/
[product-screenshot]: https://github.com/zhunhung/toaster/blob/master/images/toaster_image.jpg
