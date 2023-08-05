<h1 align="center">
    <a href="https://github.com/utsurius/django-actionable-messages">
        Actionable messages
    </a>
</h1>

<p align="center">
    <a href="https://github.com/utsurius/django-actionable-messages/blob/master/LICENSE">
        <img src="https://img.shields.io/github/license/utsurius/django-actionable-messages" alt="license"/>
    </a>
    <a href="https://github.com/utsurius/django-actionable-messages/releases">
        <img src="https://img.shields.io/github/release/utsurius/django-actionable-messages" alt="github"/>
    </a>
    <a href="https://pypi.python.org/pypi/django-actionable-messages">
        <img src="https://badge.fury.io/py/django-actionable-messages.svg" alt="pypi"/>
    </a>
</p>

1. [Base informations](#base-informations)
2. [Installation](#installation)
3. [Requirements](#requirements)
4. [Usage](#usage)
5. [AdaptiveCard](#adaptivecard)
    * [Elements](#adaptivecard-elements)
        * [TextBlock](#adaptivecard-textblock)
        * [Image](#adaptivecard-image)
        * [MediaSource](#adaptivecard-mediasource)
        * [Media](#adaptivecard-media)
        * [TextRun](#adaptivecard-textrun)
        * [RichTextBlock](#adaptivecard-richtextblock)
    * [Inputs](#adaptivecard-inputs)
        * [TextInput](#adaptivecard-textinput)
        * [NumberInput](#adaptivecard-numberinput)
        * [DateInput](#adaptivecard-dateinput)
        * [TimeInput](#adaptivecard-timeinput)
        * [ToggleInput](#adaptivecard-toggleinput)
        * [InputChoice](#adaptivecard-inputchoice)
        * [ChoiceSetInput](#adaptivecard-choicesetinput)
    * [Actions](#adaptivecard-actions)
        * [OpenUrl](#adaptivecard-openurl)
        * [Submit](#adaptivecard-submit)
        * [ShowCard](#adaptivecard-showcard)
        * [TargetElement](#adaptivecard-targetelement)
        * [ToggleVisibility](#adaptivecard-togglevisibility)
    * [Containers](#adaptivecard-containers)
        * [ActionSet](#adaptivecard-actionset)
        * [Container](#adaptivecard-container)
        * [Column](#adaptivecard-column)
        * [ColumnSet](#adaptivecard-columnset)
        * [Fact](#adaptivecard-fact)
        * [FactSet](#adaptivecard-factset)
        * [ImageSet](#adaptivecard-imageset)
    * [Types](#adaptivecard-types)
        * [BackgroundImage](#adaptivecard-backgroundimage)
    * [Cards](#adaptivecard-cards)
        * [AdaptiveCard](#adaptivecard-adaptivecard)
6. [MessageCard](#messagecard)
    * [Elements](#messagecard-elements)
        * [Header](#messagecard-header)
        * [Fact](#messagecard-fact)
        * [HeroImage](#messagecard-heroimage)
        * [InputChoice](#messagecard-inputchoice)
        * [ActionTarget](#messagecard-actiontarget)
    * [Inputs](#messagecard-inputs)
        * [TextInput](#messagecard-textinput)
        * [DateInput](#messagecard-dateinput)
        * [MultiChoiceInput](#messagecard-multichoiceinput)
    * [Actions](#messagecard-actions)
        * [OpenUri](#messagecard-openuri)
        * [HttpPOST](#messagecard-httppost)
        * [InvokeAddInCommand](#messagecard-invokeaddincommand)
        * [ActionCard](#messagecard-actioncard)
    * [Sections](#messagecard-sections)
        * [Section](#messagecard-section)
    * [Cards](#messagecard-cards)
        * [MessageCard](#messagecard-messagecard)


<h2 id="base-informations">Base informations</h2>

[Playground V2](https://messagecardplayground.azurewebsites.net/)

[Send an actionable message via email in Office 365](https://docs.microsoft.com/en-gb/outlook/actionable-messages/send-via-email)

[Outlook version requirements for actionable messages](https://docs.microsoft.com/en-us/outlook/actionable-messages/#outlook-version-requirements-for-actionable-messages)


<h2 id="installation">Installation</h2>

`pip install git+https://github.com/utsurius/django-actionable-messages`

`pip install django-actionable-messages`

Add "django_actionable_messages" to INSTALLED_APPS:

```python
INSTALLED_APPS = [
    ...
    "django_actionable_messages",
]
```

SETTINGS

```python
ACTIONABLE_MESSAGES = {
    "JSON_ENCODER": None
}
```

"JSON_ENCODER" is a doted path to custom json encoder.


<h2 id="requirements">Requirements</h2>

|Name|Version|
|---|---|
|python|3.5+|
|django|1.11.0+|


<h2 id="usage">Usage</h2>

**`examples/message_card/github.py`**

```python
from django_actionable_messages.message_card.actions import OpenUri, HttpPOST, ActionCard
from django_actionable_messages.message_card.cards import MessageCard
from django_actionable_messages.message_card.elements import Fact, ActionTarget
from django_actionable_messages.message_card.inputs import TextInput
from django_actionable_messages.message_card.sections import Section
from django_actionable_messages.message_card.utils import OSType


issue_opened = MessageCard(title="Issue opened: \"Push notifications not working\"", summary="Issue 176715375",
                           theme_color="0078D7")
issue_opened.add_section(
    Section(
        activity_title="Miguel Garcie",
        activity_subtitle="9/13/2016, 11:46am",
        activity_image="https://connectorsdemo.azurewebsites.net/images/MSC12_Oscar_002.jpg",
        text="There is a problem with Push notifications, they don't seem to be picked up by the connector.",
        facts=[
            Fact("Repository:", "mgarcia\\test"),
            Fact("Issue #:", "176715375")
        ]
    )
)
issue_opened.add_actions([
    ActionCard(
        name="Add a comment",
        inputs=[
            TextInput(input_id="comment", title="Enter a comment", is_multiline=True)
        ],
        actions=[
            HttpPOST("OK", target="http://...")
        ]
    ),
    HttpPOST("Close", target="http://..."),
    OpenUri(name="View in Github", targets=[
        ActionTarget(OSType.DEFAULT, "http://...")
    ])
])
```

**`examples/adaptive_card/calendar_reminder.py`**

```python
from django_actionable_messages.adaptive_card.actions import Submit
from django_actionable_messages.adaptive_card.cards import AdaptiveCard
from django_actionable_messages.adaptive_card.elements import TextBlock
from django_actionable_messages.adaptive_card.inputs import InputChoice, ChoiceSetInput
from django_actionable_messages.adaptive_card.utils import SCHEMA, FontSize, FontWeight, SpacingStyle, ChoiceInputStyle


calendar_reminder = AdaptiveCard(version="1.0", schema=SCHEMA)
calendar_reminder.set_speak("Your  meeting about \"Adaptive Card design session\" is starting at 12:30pm"
                            "Do you want to snooze  or do you want to send a late notification to the attendees?")
calendar_reminder.add_element(TextBlock("Adaptive Card design session", size=FontSize.LARGE, weight=FontWeight.BOLDER))
calendar_reminder.add_elements([
    TextBlock("Conf Room 112/3377 (10)", is_subtle=True),
    TextBlock("12:30 PM - 1:30 PM", is_subtle=True, spacing=SpacingStyle.NONE),
    TextBlock("Snooze for")
])
calendar_reminder.add_element(ChoiceSetInput(
    item_id="snooze", style=ChoiceInputStyle.COMPACT, value="5", choices=[
        InputChoice("5 minutes", "5"),
        InputChoice("15 minutes", "15"),
        InputChoice("30 minutes", "30")
    ]
))
calendar_reminder.add_actions([
    Submit(title="Snooze", data={
        "x": "snooze"
    }),
    Submit(title="I'll be late", data={
        "x": "late"
    })
])
```

For more view **`examples`** folder

To get dictionary, json or html payload from card use:

|Function|Type|
|---|---|
|.payload|*dict*|
|.json_payload|json string|
|.html_payload|html string - can be used to send card via email ([docs](https://docs.microsoft.com/en-gb/outlook/actionable-messages/send-via-email))|


Problem: **'... is not JSON serializable'** - probably invalid argument type was used (for example: custom object or `lazy` object instead of *str*).

Solution: [Better Python Object Serialization](https://hynek.me/articles/serialization/)

You can set JSON_ENCODER (globally) in SETTINGS(ACTIONABLE_MESSAGES) or set it by card(json_encoder):

```python
from django_actionable_messages.adaptive_card.cards import AdaptiveCard


class MyAdaptiveCard(AdaptiveCard):
    json_encoder = "path.to.my.encoder"
```
or
```python
from django_actionable_messages.adaptive_card.cards import AdaptiveCard


class MyAdaptiveCard(AdaptiveCard):
    json_encoder = MyJSONEncoder
```


Send MessageCard to msteams using webhooks and `requests` library:
```python
import requests


requests.post(
    webhook_url,
    json=card.payload,
    headers={
        "Content-Type": "application/json; charset=utf-8"
    }
)
```

To get/add `webhook_url` see here: [Get the Microsoft Teams webhook URL](https://learning.getpostman.com/docs/postman_pro/integrations/microsoft_teams/#get-the-microsoft-teams-webhook-url), [Create and add an outgoing webhook in Teams](https://support.office.com/en-ie/article/create-and-add-an-outgoing-webhook-in-teams-8e1a1648-982f-4511-b342-6d8492437207)

<h2 id="adaptivecard">AdaptiveCard</h2>

Supported versions: **1.0**, **1.1**, **1.2**

[Schema Explorer](https://adaptivecards.io/explorer/)


<h3 id="adaptivecard-elements">Elements</h3>

**src**: `from django_actionable_messages.adaptive_card.elements import ...`

<h4 id="adaptivecard-textblock">**TextBlock** ([docs](https://adaptivecards.io/explorer/TextBlock.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|**text**|set_text()|text|*str*|
|color|set_color()|color|Color<sup>1</sup>|
|font_type|set_font_type()|fontType|FontType<sup>1</sup>|
|horizontal_alignment|set_horizontal_alignment()|horizontalAlignment|HorizontalAlignment<sup>1</sup>|
|is_subtle|set_is_subtle()|isSubtle|*bool*|
|max_lines|set_max_lines()|maxLines|*int*|
|size|set_size()|size|FontSize<sup>1</sup>|
|weight|set_weight()|weight|FontWeight<sup>1</sup>|
|wrap|set_wrap()|wrap|*bool*|
|fallback|set_fallback()|fallback|FallbackOption<sup>1</sup> or card element<sup>2</sup>|
|separator|set_separator()|separator|*bool*|
|spacing|set_spacing()|spacing|SpacingStyle<sup>1</sup>|
|item_id|set_id()|id|*str*|
|is_visible|set_is_visible()|isVisible|*bool*|
|requires|set_requires()|requires|*dict*|
|height|set_height()|height|BlockElementHeight<sup>1</sup>|

\[1\] `from django_actionable_messages.adaptive_cards.utils import ...`

\[2\]

|Type|All except|Import|
|---|---|---|
|`containers`|Fact, Column|`from django_actionable_messages.adaptive_cards.containers import ...`|
|`elements`|MediaSource, TextRun|`from django_actionable_messages.adaptive_cards.elements import ...`|
|`inputs`|InputChoice|`from django_actionable_messages.adaptive_cards.inputs import ...`|

<h4 id="adaptivecard-image">**Image** ([docs](https://adaptivecards.io/explorer/Image.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|**url**|set_url()|url|*str*|
|alternate_text|set_alternate_text()|altText|*str*|
|background_color|set_background_color()|backgroundColor|*str*|
|height|set_height()|height|str or BlockElementHeight<sup>1</sup>|
|horizontal_alignment|set_horizontal_alignment()|horizontalAlignment|HorizontalAlignment<sup>1</sup>|
|select_action|set_select_action()|selectAction|see docs|
|size|set_size()|size|ImageSize<sup>1</sup>|
|style|set_style()|style|ImageStyle<sup>1</sup>|
|width|set_width()|width|*str*|
|fallback|set_fallback()|fallback|FallbackOption<sup>1</sup> or card element<sup>2</sup>|
|separator|set_separator()|separator|*bool*|
|spacing|set_spacing()|spacing|SpacingStyle<sup>1</sup>|
|item_id|set_id()|id|*str*|
|is_visible|set_is_visible()|isVisible|*bool*|
|requires|set_requires()|requires|*dict*|
|height|set_height()|height|BlockElementHeight<sup>1</sup>|

\[1\] `from django_actionable_messages.adaptive_cards.utils import ...`

\[2\]

|Type|All except|Import|
|---|---|---|
|`containers`|Fact, Column|`from django_actionable_messages.adaptive_cards.containers import ...`|
|`elements`|MediaSource, TextRun|`from django_actionable_messages.adaptive_cards.elements import ...`|
|`inputs`|InputChoice|`from django_actionable_messages.adaptive_cards.inputs import ...`|

<h4 id="adaptivecard-mediasource">**MediaSource** ([docs](https://adaptivecards.io/explorer/MediaSource.html))</h4>

|Argument name|Property|Type|
|---|---|---|
|**mime_type**|mimeType|*str*|
|**url**|url|*str*|

<h4 id="adaptivecard-media">**Media** ([docs](https://adaptivecards.io/explorer/Media.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|**sources**|add_sources()|sources|*list* of MediaSource(s)<sup>1</sup>|
|poster|set_poster()|poster|*str*|
|alternate_text|set_alternate_text()|altText|*str*|
|fallback|set_fallback()|fallback|FallbackOption<sup>2</sup> or card element<sup>3</sup>|
|separator|set_separator()|separator|*bool*|
|spacing|set_spacing()|spacing|SpacingStyle<sup>2</sup>|
|item_id|set_id()|id|*str*|
|is_visible|set_is_visible()|isVisible|*bool*|
|requires|set_requires()|requires|*dict*|
|height|set_height()|height|BlockElementHeight<sup>2</sup>|

Other functions

|Name|Property|Type|
|---|---|---|
|add_source()|sources|MediaSource<sup>1</sup>|

\[1\] `from django_actionable_messages.adaptive_cards.elements import ...`

\[2\] `from django_actionable_messages.adaptive_cards.utils import ...`

\[3\]

|Type|All except|Import|
|---|---|---|
|`containers`|Fact, Column|`from django_actionable_messages.adaptive_cards.containers import ...`|
|`elements`|MediaSource, TextRun|`from django_actionable_messages.adaptive_cards.elements import ...`|
|`inputs`|InputChoice|`from django_actionable_messages.adaptive_cards.inputs import ...`|

<h4 id="adaptivecard-textrun">**TextRun** ([docs](https://adaptivecards.io/explorer/TextRun.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|**text**|set_text()|text|*str*|
|color|set_color()|color|Color<sup>1</sup>|
|font_type|set_font_type()|fontType|FontType<sup>1</sup>|
|highlight|set_highlight()|highlight|*bool*|
|is_subtle|set_is_subtle()|isSubtle|*bool*|
|italic|set_italic()|italic|*bool*|
|select_action|set_select_action()|selectAction|see docs|
|size|set_size()|fontSize|FontSize<sup>1</sup>|
|strike_through|set_strike_through()|strikethrough|*bool*|
|weight|set_weight()|fontWeight|FontWeight<sup>1</sup>|

\[1\] `from django_actionable_messages.adaptive_cards.utils import ...`

<h4 id="adaptivecard-richtextblock">**RichTextBlock** ([docs](https://adaptivecards.io/explorer/RichTextBlock.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|**inlines**|set_inlines()|inlines|*str*, TextRun<sup>1</sup>|
|horizontal_alignment|set_horizontal_alignment()|horizontalAlignment|HorizontalAlignment<sup>1</sup>|
|fallback|set_fallback()|fallback|FallbackOption<sup>2</sup> or card element<sup>3</sup>|
|separator|set_separator()|separator|*bool*|
|spacing|set_spacing()|spacing|SpacingStyle<sup>2</sup>|
|item_id|set_id()|id|*str*|
|is_visible|set_is_visible()|isVisible|*bool*|
|requires|set_requires()|requires|*dict*|
|height|set_height()|height|BlockElementHeight<sup>1</sup>|

\[1\] `from django_actionable_messages.adaptive_cards.elements import ...`

\[2\] `from django_actionable_messages.adaptive_cards.utils import ...`

\[3\]

|Type|All except|Import|
|---|---|---|
|`containers`|Fact, Column|`from django_actionable_messages.adaptive_cards.containers import ...`|
|`elements`|MediaSource, TextRun|`from django_actionable_messages.adaptive_cards.elements import ...`|
|`inputs`|InputChoice|`from django_actionable_messages.adaptive_cards.inputs import ...`|

<h3 id="adaptivecard-inputs">Inputs</h3>

**src**: `from django_actionable_messages.adaptive_card.inputs import ...`

<h4 id="adaptivecard-textinput">**TextInput** ([docs](https://adaptivecards.io/explorer/Input.Text.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|is_multiline|set_is_multiline()|isMultiline|*bool*|
|max_length|set_max_length()|maxLength|*int*|
|placeholder|set_placeholder()|placeholder|*str*|
|style|set_style()|style|TextInputStyle<sup>1</sup>|
|inline_action|set_inline_action()|inlineAction|see docs|
|value|set_value()|value|*str*|
|fallback|set_fallback()|fallback|FallbackOption<sup>1</sup> or card element<sup>2</sup>|
|separator|set_separator()|separator|*bool*|
|spacing|set_spacing()|spacing|SpacingStyle<sup>1</sup>|
|item_id|set_id()|id|*str*|
|is_visible|set_is_visible()|isVisible|*bool*|
|requires|set_requires()|requires|*dict*|
|height|set_height()|height|BlockElementHeight<sup>1</sup>|

\[1\] `from django_actionable_messages.adaptive_cards.utils import ...`

\[2\]

|Type|All except|Import|
|---|---|---|
|`containers`|Fact, Column|`from django_actionable_messages.adaptive_cards.containers import ...`|
|`elements`|MediaSource, TextRun|`from django_actionable_messages.adaptive_cards.elements import ...`|
|`inputs`|InputChoice|`from django_actionable_messages.adaptive_cards.inputs import ...`|

<h4 id="adaptivecard-numberinput">**NumberInput** ([docs](https://adaptivecards.io/explorer/Input.Number.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|max_value|set_max_value()|maxValue|*int*|
|min_value|set_min_value()|minValue|*int*|
|placeholder|set_placeholder()|placeholder|*str*|
|value|set_value()|value|*int*|
|fallback|set_fallback()|fallback|FallbackOption<sup>1</sup> or card element<sup>2</sup>|
|separator|set_separator()|separator|*bool*|
|spacing|set_spacing()|spacing|SpacingStyle<sup>1</sup>|
|item_id|set_id()|id|*str*|
|is_visible|set_is_visible()|isVisible|*bool*|
|requires|set_requires()|requires|*dict*|
|height|set_height()|height|BlockElementHeight<sup>1</sup>|

\[1\] `from django_actionable_messages.adaptive_cards.utils import ...`

\[2\]

|Type|All except|Import|
|---|---|---|
|`containers`|Fact, Column|`from django_actionable_messages.adaptive_cards.containers import ...`|
|`elements`|MediaSource, TextRun|`from django_actionable_messages.adaptive_cards.elements import ...`|
|`inputs`|InputChoice|`from django_actionable_messages.adaptive_cards.inputs import ...`|

<h4 id="adaptivecard-dateinput">**DateInput** ([docs](https://adaptivecards.io/explorer/Input.Date.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|max_value|set_max_value()|maxValue|*str*|
|min_value|set_min_value()|minValue|*str*|
|placeholder|set_placeholder()|placeholder|*str*|
|value|set_value()|value|*str*|
|fallback|set_fallback()|fallback|FallbackOption<sup>1</sup> or card element<sup>2</sup>|
|separator|set_separator()|separator|*bool*|
|spacing|set_spacing()|spacing|SpacingStyle<sup>1</sup>|
|item_id|set_id()|id|*str*|
|is_visible|set_is_visible()|isVisible|*bool*|
|requires|set_requires()|requires|*dict*|
|height|set_height()|height|BlockElementHeight<sup>1</sup>|

\[1\] `from django_actionable_messages.adaptive_cards.utils import ...`

\[2\]

|Type|All except|Import|
|---|---|---|
|`containers`|Fact, Column|`from django_actionable_messages.adaptive_cards.containers import ...`|
|`elements`|MediaSource, TextRun|`from django_actionable_messages.adaptive_cards.elements import ...`|
|`inputs`|InputChoice|`from django_actionable_messages.adaptive_cards.inputs import ...`|

<h4 id="adaptivecard-timeinput">**TimeInput** ([docs](https://adaptivecards.io/explorer/Input.Time.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|max_value|set_max_value()|maxValue|*str*|
|min_value|set_min_value()|minValue|*str*|
|placeholder|set_placeholder()|placeholder|*str*|
|value|set_value()|value|*str*|
|fallback|set_fallback()|fallback|FallbackOption<sup>1</sup> or card element<sup>2</sup>|
|separator|set_separator()|separator|*bool*|
|spacing|set_spacing()|spacing|SpacingStyle<sup>1</sup>|
|item_id|set_id()|id|*str*|
|is_visible|set_is_visible()|isVisible|*bool*|
|requires|set_requires()|requires|*dict*|
|height|set_height()|height|BlockElementHeight<sup>1</sup>|

\[1\] `from django_actionable_messages.adaptive_cards.utils import ...`

\[2\]

|Type|All except|Import|
|---|---|---|
|`containers`|Fact, Column|`from django_actionable_messages.adaptive_cards.containers import ...`|
|`elements`|MediaSource, TextRun|`from django_actionable_messages.adaptive_cards.elements import ...`|
|`inputs`|InputChoice|`from django_actionable_messages.adaptive_cards.inputs import ...`|

<h4 id="adaptivecard-toggleinput">**ToggleInput** ([docs](https://adaptivecards.io/explorer/Input.Toggle.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|**title**|set_title()|title|*str*|
|value|set_value()|value|*str*|
|value_off|set_value_off()|valueOff|*str*|
|value_on|set_value_on()|valueOn|*str*|
|wrap|set_wrap()|wrap|*bool*|
|fallback|set_fallback()|fallback|FallbackOption<sup>1</sup> or card element<sup>2</sup>|
|separator|set_separator()|separator|*bool*|
|spacing|set_spacing()|spacing|SpacingStyle<sup>1</sup>|
|item_id|set_id()|id|*str*|
|is_visible|set_is_visible()|isVisible|*bool*|
|requires|set_requires()|requires|*dict*|
|height|set_height()|height|BlockElementHeight<sup>1</sup>|

\[1\] `from django_actionable_messages.adaptive_cards.utils import ...`

\[2\]

|Type|All except|Import|
|---|---|---|
|`containers`|Fact, Column|`from django_actionable_messages.adaptive_cards.containers import ...`|
|`elements`|MediaSource, TextRun|`from django_actionable_messages.adaptive_cards.elements import ...`|
|`inputs`|InputChoice|`from django_actionable_messages.adaptive_cards.inputs import ...`|

<h4 id="adaptivecard-inputchoice">**InputChoice** ([docs](https://adaptivecards.io/explorer/Input.Choice.html))</h4>

|Argument name|Property|Type|
|---|---|---|
|**title**|title|*str*|
|**value**|value|*str*, *int*|

<h4 id="adaptivecard-choicesetinput">**ChoiceSetInput** ([docs](https://adaptivecards.io/explorer/Input.ChoiceSet.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|**choices**|set_choices()|choices|*list* of InputChoice(s)<sup>1</sup>|
|is_multi_select|set_is_multi_select()|isMultiSelect|*bool*|
|style|set_style()|style|ChoiceInputStyle<sup>2</sup>|
|value|set_value()|value|*str*|
|wrap|set_wrap()|wrap|*bool*|
|fallback|set_fallback()|fallback|FallbackOption<sup>2</sup> or card element<sup>3</sup>|
|separator|set_separator()|separator|*bool*|
|spacing|set_spacing()|spacing|SpacingStyle<sup>2</sup>|
|item_id|set_id()|id|*str*|
|is_visible|set_is_visible()|isVisible|*bool*|
|requires|set_requires()|requires|*dict*|
|height|set_height()|height|BlockElementHeight<sup>2</sup>|

\[1\] `from django_actionable_messages.adaptive_cards.inputs import ...`

\[2\] `from django_actionable_messages.adaptive_cards.utils import ...`

\[3\]

|Type|All except|Import|
|---|---|---|
|`containers`|Fact, Column|`from django_actionable_messages.adaptive_cards.containers import ...`|
|`elements`|MediaSource, TextRun|`from django_actionable_messages.adaptive_cards.elements import ...`|
|`inputs`|InputChoice|`from django_actionable_messages.adaptive_cards.inputs import ...`|


<h3 id="adaptivecard-actions">Actions</h3>

**src**: `from django_actionable_messages.adaptive_card.actions import ...`

<h4 id="adaptivecard-openurl">**OpenUrl** ([docs](https://adaptivecards.io/explorer/Action.OpenUrl.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|**url**|set_url()|url|*str*|
|title|set_title()|title|*str*|
|icon_url|set_icon_url()|iconUrl|*str*|
|style|set_style()|style|ActionStyle<sup>2</sup>|
|item_id|set_id()|id|*str*|
|fallback|set_fallback()|fallback|FallbackOption<sup>2</sup> or action<sup>1</sup>(except TargetElement<sup>1</sup>)|
|requires|set_requires()|requires|*dict*|

\[1\] `from django_actionable_messages.adaptive_cards.actions import ...`

\[2\] `from django_actionable_messages.adaptive_cards.utils import ...`

<h4 id="adaptivecard-submit">**Submit** ([docs](https://adaptivecards.io/explorer/Action.Submit.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|data|set_data()|data|*str*, *dict*|
|title|set_title()|title|*str*|
|icon_url|set_icon_url()|iconUrl|*str*|
|style|set_style()|style|ActionStyle<sup>2</sup>|
|item_id|set_id()|id|*str*|
|fallback|set_fallback()|fallback|FallbackOption<sup>2</sup> or action<sup>1</sup>(except TargetElement<sup>1</sup>)|
|requires|set_requires()|requires|*dict*|

\[1\] `from django_actionable_messages.adaptive_cards.actions import ...`

\[2\] `from django_actionable_messages.adaptive_cards.utils import ...`

<h4 id="adaptivecard-showcard">**ShowCard** ([docs](https://adaptivecards.io/explorer/Action.ShowCard.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|card|set_card()|card|AdaptiveCard<sup>2</sup>|
|title|set_title()|title|*str*|
|icon_url|set_icon_url()|iconUrl|*str*|
|style|set_style()|style|ActionStyle<sup>3</sup>|
|item_id|set_id()|id|*str*|
|fallback|set_fallback()|fallback|FallbackOption<sup>3</sup> or action<sup>1</sup>(except TargetElement<sup>1</sup>)|
|requires|set_requires()|requires|*dict*|

\[1\] `from django_actionable_messages.adaptive_cards.actions import ...`

\[2\] `from django_actionable_messages.adaptive_cards.cards import ...`

\[3\] `from django_actionable_messages.adaptive_cards.utils import ...`

<h4 id="adaptivecard-targetelement">**TargetElement** ([docs](https://adaptivecards.io/explorer/TargetElement.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|**element_id**|set_element_id()|elementId|*str*|
|is_visible|set_is_visible()|isVisible|*bool*|

<h4 id="adaptivecard-togglevisibility">**ToggleVisibility** ([docs](https://adaptivecards.io/explorer/Action.ToggleVisibility.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|target_elements|set_target_elements()|targetElements|*list* of TargetElement<sup>1</sup>/str (can be mixed)|
|title|set_title()|title|*str*|
|icon_url|set_icon_url()|iconUrl|*str*|
|style|set_style()|style|ActionStyle<sup>2</sup>|
|item_id|set_id()|id|*str*|
|fallback|set_fallback()|fallback|FallbackOption<sup>1</sup> or action<sup>1</sup>(except TargetElement<sup>1</sup>)|
|requires|set_requires()|requires|*dict*|

\[1\] `from django_actionable_messages.adaptive_cards.actions import ...`

\[2\] `from django_actionable_messages.adaptive_cards.utils import ...`


<h3 id="adaptivecard-containers">Containers</h3>

**src**: `from django_actionable_messages.adaptive_card.containers import ...`

<h4 id="adaptivecard-actionset">**ActionSet** ([docs](https://adaptivecards.io/explorer/ActionSet.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|actions|add_actions()|actions|*list* of actions(see docs)|
|fallback|set_fallback()|fallback|FallbackOption<sup>1</sup> or card element<sup>2</sup>|
|separator|set_separator()|separator|*bool*|
|spacing|set_spacing()|spacing|SpacingStyle<sup>1</sup>|
|item_id|set_id()|id|*str*|
|is_visible|set_is_visible()|isVisible|*bool*|
|requires|set_requires()|requires|*dict*|
|height|set_height()|height|BlockElementHeight<sup>1</sup>|

Other functions

|Name|Property|Type|
|---|---|---|
|add_action()|actions|see docs|

\[1\] `from django_actionable_messages.adaptive_cards.utils import ...`

\[2\]

|Type|All except|Import|
|---|---|---|
|`containers`|Fact, Column|`from django_actionable_messages.adaptive_cards.containers import ...`|
|`elements`|MediaSource, TextRun|`from django_actionable_messages.adaptive_cards.elements import ...`|
|`inputs`|InputChoice|`from django_actionable_messages.adaptive_cards.inputs import ...`|

<h4 id="adaptivecard-container">**Container** ([docs](https://adaptivecards.io/explorer/Container.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|items|add_items()|items|see docs|
|select_action|set_select_action()|selectAction|any action(see docs)|
|style|set_style()|style|Style<sup>2</sup>|
|vertical_content_alignment|set_vertical_content_alignment()|verticalContentAlignment|VerticalAlignment<sup>2</sup>|
|bleed|set_bleed()|bleed|*bool*|
|background_image|set_background_image()|backgroundImage|BackgroundImage<sup>1</sup>|
|min_height|set_min_height()|minHeight|*str*|
|fallback|set_fallback()|fallback|FallbackOption<sup>2</sup> or card element<sup>3</sup>|
|separator|set_separator()|separator|*bool*|
|spacing|set_spacing()|spacing|SpacingStyle<sup>2</sup>|
|item_id|set_id()|id|*str*|
|is_visible|set_is_visible()|isVisible|*bool*|
|requires|set_requires()|requires|*dict*|
|height|set_height()|height|BlockElementHeight<sup>2</sup>|

Other functions

|Name|Property|Type|
|---|---|---|
|add_item()|items|see docs|

\[1\] `from django_actionable_messages.adaptive_cards.types import ...`

\[2\] `from django_actionable_messages.adaptive_cards.utils import ...`

\[3\]

|Type|All except|Import|
|---|---|---|
|`containers`|Fact, Column|`from django_actionable_messages.adaptive_cards.containers import ...`|
|`elements`|MediaSource, TextRun|`from django_actionable_messages.adaptive_cards.elements import ...`|
|`inputs`|InputChoice|`from django_actionable_messages.adaptive_cards.inputs import ...`|

<h4 id="adaptivecard-column">**Column** ([docs](https://adaptivecards.io/explorer/Column.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|items|add_items()|items|*list* (see docs)|
|background_image|set_background_image()|backgroundImage|*str*, BackgroundImage<sup>2</sup>|
|bleed|set_bleed()|bleed|*bool*|
|fallback|set_fallback()|fallback|FallbackOption<sup>3</sup> or Column<sup>1</sup>|
|min_height|set_min_height()|minHeight|*str*|
|separator|set_separator()|separator|*bool*|
|spacing|set_spacing()|spacing|SpacingStyle<sup>3</sup>|
|select_action|set_select_action()|selectAction|see docs|
|style|set_style()|style|Style<sup>3</sup>|
|vertical_content_alignment|set_vertical_content_alignment()|verticalContentAlignment|VerticalAlignment<sup>3</sup>|
|width|set_width()|width|*str*, *int*, Width<sup>3</sup>|
|item_id|set_id()|id|*str*|
|is_visible|set_is_visible()|isVisible|*bool*|
|requires|set_requires()|requires|*dict*|

\[1\] `from django_actionable_messages.adaptive_cards.containers import ...`

\[2\] `from django_actionable_messages.adaptive_cards.types import ...`

\[3\] `from django_actionable_messages.adaptive_cards.utils import ...`

<h4 id="adaptivecard-columnset">**ColumnSet** ([docs](https://adaptivecards.io/explorer/ColumnSet.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|**columns**|add_columns()|columns|*list* of Column(s)<sup>1</sup>|
|select_action|set_select_action()|selectAction|see docs|
|style|set_style()|style|Style<sup>2</sup>|
|bleed|set_bleed()|bleed|*bool*|
|min_height|set_min_height()|minHeight|*str*|
|fallback|set_fallback()|fallback|FallbackOption<sup>2</sup> or card element<sup>3</sup>|
|separator|set_separator()|separator|*bool*|
|spacing|set_spacing()|spacing|SpacingStyle<sup>2</sup>|
|item_id|set_id()|id|*str*|
|is_visible|set_is_visible()|isVisible|*bool*|
|requires|set_requires()|requires|*dict*|
|height|set_height()|height|BlockElementHeight<sup>2</sup>|

Other functions

|Name|Property|Type|
|---|---|---|
|add_column()|columns|Column<sup>1</sup>|

\[1\] `from django_actionable_messages.adaptive_cards.containers import ...`

\[2\] `from django_actionable_messages.adaptive_cards.utils import ...`

\[3\]

|Type|All except|Import|
|---|---|---|
|`containers`|Fact, Column|`from django_actionable_messages.adaptive_cards.containers import ...`|
|`elements`|MediaSource, TextRun|`from django_actionable_messages.adaptive_cards.elements import ...`|
|`inputs`|InputChoice|`from django_actionable_messages.adaptive_cards.inputs import ...`|

<h4 id="adaptivecard-fact">**Fact** ([docs](https://adaptivecards.io/explorer/Fact.html))</h4>

|Argument name|Property|Type|
|---|---|---|
|**title**|title|*str*|
|**value**|value|*str*|

<h4 id="adaptivecard-factset">**FactSet** ([docs](https://adaptivecards.io/explorer/FactSet.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|facts|add_facts()|facts|*list* of Fact(s)<sup>1</sup>|
|fallback|set_fallback()|fallback|FallbackOption<sup>2</sup> or card element<sup>3</sup>|
|separator|set_separator()|separator|*bool*|
|spacing|set_spacing()|spacing|SpacingStyle<sup>2</sup>|
|item_id|set_id()|id|*str*|
|is_visible|set_is_visible()|isVisible|*bool*|
|requires|set_requires()|requires|*dict*|
|height|set_height()|height|BlockElementHeight<sup>2</sup>|

Other functions

|Name|Property|Type|
|---|---|---|
|add_fact()|facts|Fact<sup>1</sup>|

\[1\] `from django_actionable_messages.adaptive_cards.containers import ...`

\[2\] `from django_actionable_messages.adaptive_cards.utils import ...`

\[3\]

|Type|All except|Import|
|---|---|---|
|`containers`|Fact, Column|`from django_actionable_messages.adaptive_cards.containers import ...`|
|`elements`|MediaSource, TextRun|`from django_actionable_messages.adaptive_cards.elements import ...`|
|`inputs`|InputChoice|`from django_actionable_messages.adaptive_cards.inputs import ...`|

<h4 id="adaptivecard-imageset">**ImageSet** ([docs](https://adaptivecards.io/explorer/ImageSet.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|images|add_images()|images|*list* of Image(s)<sup>1</sup>|
|image_size|set_image_size()|imageSize|ImageSize<sup>2</sup>|
|fallback|set_fallback()|fallback|FallbackOption<sup>2</sup> or card element<sup>3</sup>|
|separator|set_separator()|separator|*bool*|
|spacing|set_spacing()|spacing|SpacingStyle<sup>2</sup>|
|item_id|set_id()|id|*str*|
|is_visible|set_is_visible()|isVisible|*bool*|
|requires|set_requires()|requires|*dict*|
|height|set_height()|height|BlockElementHeight<sup>2</sup>|

Other functions

|Name|Property|Type|
|---|---|---|
|add_image()|images|Image<sup>1</sup>|

\[1\] `from django_actionable_messages.adaptive_cards.elements import ...`

\[2\] `from django_actionable_messages.adaptive_cards.utils import ...`

\[3\]

|Type|All except|Import|
|---|---|---|
|`containers`|Fact, Column|`from django_actionable_messages.adaptive_cards.containers import ...`|
|`elements`|MediaSource, TextRun|`from django_actionable_messages.adaptive_cards.elements import ...`|
|`inputs`|InputChoice|`from django_actionable_messages.adaptive_cards.inputs import ...`|


<h3 id="adaptivecard-types">Types</h3>

**src**: `from django_actionable_messages.adaptive_card.types import ...`

<h4 id="adaptivecard-backgroundimage">**BackgroundImage** ([docs](https://adaptivecards.io/explorer/BackgroundImage.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|**url**|set_url()|url|*str*|
|fill_mode|set_fill_mode()|fillMode|FillMode<sup>1</sup>|
|horizontal_alignment|set_horizontal_alignment()|horizontalAlignment|HorizontalAlignment<sup>1</sup>|
|vertical_alignment|set_vertical_alignment()|verticalAlignment|VerticalAlignment<sup>1</sup>|

\[1\] `from django_actionable_messages.adaptive_cards.utils import ...`

<h3 id="adaptivecard-cards">Cards</h3>

**src**: `from django_actionable_messages.adaptive_card.cards import ...`

<h4 id="adaptivecard-adaptivecard">**AdaptiveCard** ([docs](https://adaptivecards.io/explorer/AdaptiveCard.html))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|version|set_version()|version|*str*, SCHEMA<sup>1</sup>|
|schema|set_schema()|$schema|*str*|
|inputs|add_elements()|inputs|*list* of inputs(see docs)|
|actions|add_actions()|actions|*list* of actions(see docs)|
|select_action|set_select_action()|selectAction|see docs|
|style|set_style()|style|Style<sup>1</sup>|
|hide_original_body|set_hide_original_body()|hideOriginalBody|*bool*|
|fallback_text|set_fallback_text()|fallbackText|*str*|
|background_image|set_background_image()|backgroundImage|*str*, Image<sup>2</sup>|
|min_height|set_min_height()|minHeight|*str*|
|speak|set_speak()|speak|*str*|
|lang|set_lang()|lang|*str*|
|vertical_content_alignment|set_vertical_content_alignment()|verticalContentAlignment|VerticalAlignment<sup>1</sup>|

AdaptiveCard also have other functions:

|Name|Property|Type|
|---|---|---|
|add_element()|body|any input(see docs)|
|add_action()|actions|any action(see docs)|

\[1\] `from django_actionable_messages.adaptive_cards.utils import ...`

\[2\] `from django_actionable_messages.adaptive_cards.elements import ...`

<h2 id="messagecard">MessageCard</h2>

[Legacy actionable message card reference](https://docs.microsoft.com/en-gb/outlook/actionable-messages/message-card-reference)

<h3 id="messagecard-elements">Elements</h3>

**src**: `from django_actionable_messages.message_card.elements import ...`

<h4 id="messagecard-header">**Header** ([docs](https://docs.microsoft.com/en-gb/outlook/actionable-messages/message-card-reference#header))</h4>

|Argument name|Property|Type|
|---|---|---|
|**name**|name|*str*|
|value|value|*str*, *int*|

<h4 id="messagecard-fact">**Fact**</h4>

|Argument name|Property|Type|
|---|---|---|
|**name**|name|*str*|
|**value**|value|*str*|

<h4 id="messagecard-heroimage">**HeroImage** ([docs](https://docs.microsoft.com/en-gb/outlook/actionable-messages/message-card-reference#image-object))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|**url**|set_url()|image|*str*|
|title|set_title()|title|*str*|

<h4 id="messagecard-inputchoice">**InputChoice**</h4>

|Argument name|Property|Type|
|---|---|---|
|**name**|display|*str*|
|**value**|value|*str*, *int*|

<h4 id="messagecard-actiontarget">**ActionTarget**</h4>

|Argument name|Property|Type|
|---|---|---|
|**os_type**|os|OSType<sup>1</sup>|
|url|uri|*str*|

\[1\] `from django_actionable_messages.message_cards.utils import ...`

<h3 id="messagecard-inputs">Inputs</h3>

**src**: `from django_actionable_messages.message_card.inputs import ...`

<h4 id="messagecard-textinput">**TextInput** ([docs](https://docs.microsoft.com/en-gb/outlook/actionable-messages/message-card-reference#textinput))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|max_length|set_max_length()|maxLength|*int*|
|is_multiline|set_is_multiline()|isMultiline|*bool*|
|input_id|set_id()|id|*str*|
|title|set_title()|title|*str*|
|value|set_value()|value|*str*|
|is_required|set_is_required()|isRequired|*bool*|

<h4 id="messagecard-dateinput">**DateInput** ([docs](https://docs.microsoft.com/en-gb/outlook/actionable-messages/message-card-reference#dateinput))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|include_time|set_include_time()|maxLength|*bool*|
|input_id|set_id()|id|*str*|
|title|set_title()|title|*str*|
|value|set_value()|value|*str*|
|is_required|set_is_required()|isRequired|*bool*|

<h4 id="messagecard-multichoiceinput">**MultiChoiceInput** ([docs](https://docs.microsoft.com/en-gb/outlook/actionable-messages/message-card-reference#multichoiceinput))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|**choices**|add_choices()|choices|*list* of InputChoice(s)<sup>1</sup>|
|is_multi_select|set_is_multi_select()|isMultiSelect|*bool*|
|style|set_style()|style|ChoiceStyle<sup>2</sup>|
|input_id|set_id()|id|*str*|
|title|set_title()|title|*str*|
|value|set_value()|value|*str*|
|is_required|set_is_required()|isRequired|*bool*|

Other functions

|Name|Property|Type|
|---|---|---|
|add_choice()|choices|InputChoice<sup>1</sup>|

\[1\] `from django_actionable_messages.message_cards.inputs import ...`

\[2\] `from django_actionable_messages.message_cards.utils import ...`

<h3 id="messagecard-actions">Actions</h3>

**src**: `from django_actionable_messages.message_card.actions import ...`

<h4 id="messagecard-openuri">**OpenUri** ([docs](https://docs.microsoft.com/en-gb/outlook/actionable-messages/message-card-reference#openuri-action))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|**name**|set_name()|name|*str*|
|targets|add_targets()|targets|*list* of ActionTarget<sup>1</sup>|

Other functions

|Name|Property|Type|
|---|---|---|
|add_target()|targets|ActionTarget<sup>1</sup>|


\[1\] `from django_actionable_messages.message_cards.elements import ...`

<h4 id="messagecard-httppost">**HttpPOST** ([docs](https://docs.microsoft.com/en-gb/outlook/actionable-messages/message-card-reference#httppost-action))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|**name**|set_name()|name|*str*|
|**target**|set_target()|targets|*str*|
|headers|add_headers()|headers|*list* of Header(s)<sup>1</sup>|
|body|set_body()|body|*str*|
|body_content_type|set_body_content_type()|bodyContentType|*str*|

Other functions

|Name|property|Type|
|---|---|---|
|add_header()|headers|Header<sup>1</sup>|

\[1\] `from django_actionable_messages.message_cards.elements import ...`

<h4 id="messagecard-invokeaddincommand">**InvokeAddInCommand** ([docs](https://docs.microsoft.com/en-gb/outlook/actionable-messages/message-card-reference#invokeaddincommand-action))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|**name**|set_name()|name|*str*|
|**add_in_id**|set_add_in_id()|addInId|*str*|
|**desktop_command_id**|set_desktop_command_id()|desktopCommandId|*str*|
|initialization_context|set_set_initialization_context()|initializationContext|*dict*|

<h4 id="messagecard-actioncard">**ActionCard** ([docs](https://docs.microsoft.com/en-gb/outlook/actionable-messages/message-card-reference#actioncard-action))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|**name**|set_name()|name|*str*|
|inputs|add_inputs()|inputs|*list* of inputs(see docs)|
|actions|add_actions()|actions|*list* of actions(see docs)|

Other functions

|Name|Property|Type|
|---|---|---|
|add_input()|inputs|see docs|
|add_action()|actions|see docs|


<h3 id="messagecard-sections">Sections</h3>

**src**: `from django_actionable_messages.message_card.sections import ...`

<h4 id="messagecard-section">**Section** ([docs](https://docs.microsoft.com/en-gb/outlook/actionable-messages/message-card-reference#section-fields))</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|start_group|set_start_group()|startGroup|*bool*|
|title|set_title()|title|*str*|
|text|set_text()|text|*str*|
|activity_image|set_activity_image()|activityImage|*str*|
|activity_title|set_activity_title()|activityTitle|*str*|
|activity_subtitle|set_activity_subtitle()|activitySubtitle|*str*|
|activity_text|set_activity_text()|activityText|*str*|
|hero_image|set_hero_image()|heroImage|HeroImage<sup>1</sup>|
|facts|add_facts()|facts|*list* of Fact(s)<sup>1</sup>|
|actions|add_potential_actions()|potentialAction|*list* of actions(see docs)|

Other functions:

|Name|Property|Type|
|---|---|---|
|set_activity(image, title, subtitle, text)|activityImage, activityTitle, activitySubtitle, activityText|*str*|
|add_fact()|facts|Fact<sup>1</sup>|
|add_action()|potentialAction|any action(see docs)|

\[1\] `from django_actionable_messages.message_cards.elements import ...`

<h3 id="messagecard-cards">Cards</h3>

**src**: `from django_actionable_messages.message_card.cards import ...`

<h4 id="messagecard-messagecard">**MessageCard**</h4>

|Argument name|Function|Property|Type|
|---|---|---|---|
|title|set_title()|title|*str*|
|text|set_text()|text|*str*|
|originator|set_originator()|originator|*str*|
|summary|set_summary()|summary|*str*|
|theme_color|set_theme_color()|themeColor|*str*|
|correlation_id|set_correlation_id()|correlationId|*str*|
|auto_correlation_id*|-|correlationId|*bool* (default: *True*)|
|expected_actors|set_expected_actors()|expectedActors|*list* of emails|
|hide_original_body|set_hide_original_body()|hideOriginalBody|*bool*|
|sections|add_sections()|sections|*list* of Section(s)<sup>1</sup>|
|actions|add_actions()|potentialAction|*list* of actions(see docs)|

Other functions:

|Name|Property|Type|
|---|---|---|
|add_section()|sections|Section<sup>1</sup>|
|add_action()|potentialAction|any action(see docs)|

\[1\] `from django_actionable_messages.message_cards.sections import ...`
