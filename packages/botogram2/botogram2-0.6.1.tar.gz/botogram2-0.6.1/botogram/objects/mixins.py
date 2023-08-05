# Copyright (c) 2015-2019 The Botogram Authors (see AUTHORS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.

import importlib
import json

from .. import syntaxes
from .. import utils
from ..utils.deprecations import _deprecated_message
from .base import multiple

_objects_module = None


def _objects():
    global _objects_module

    # This is lazily loaded to avoid circular dependencies
    if _objects_module is None:
        _objects_module = importlib.import_module("..objects", __package__)

    return _objects_module


def _require_api(func):
    """Decorator which forces to have the api on an object"""
    @utils.wraps(func)
    def __(self, *args, **kwargs):
        if not hasattr(self, "_api") or self._api is None:
            raise RuntimeError("An API instance must be provided")
        return func(self, *args, **kwargs)
    return __


class ChatMixin:
    """Add some methods for chats"""

    def _get_call_args(self, reply_to, extra, attach, notify):
        """Get default API call arguments"""
        # Convert instance of Message to ids in reply_to
        if hasattr(reply_to, "id"):
            reply_to = reply_to.id

        args = {"chat_id": self.id}
        if reply_to is not None:
            args["reply_to_message_id"] = reply_to
        if extra is not None:
            _deprecated_message(
                "The extra parameter", "1.0", "use the attach parameter", -4
            )
            args["reply_markup"] = json.dumps(extra.serialize())
        if attach is not None:
            if not hasattr(attach, "_serialize_attachment"):
                raise ValueError("%s is not an attachment" % attach)
            args["reply_markup"] = json.dumps(attach._serialize_attachment(
                self
            ))
        if not notify:
            args["disable_notification"] = True

        return args

    @staticmethod
    def _get_file_args(path, file_id, url):
        args = None
        if path is not None and file_id is None and url is None:
            file = open(path, "rb")
        elif file_id is not None and path is None and url is None:
            args = file_id
            file = None
        elif url is not None and file_id is None and path is None:
            args = url
            file = None
        elif path is None and file_id is None and url is None:
            raise TypeError("path or file_id or URL is missing")
        else:
            raise TypeError("Only one among path, file_id and URL must be" +
                            "passed")
        return args, file

    @_require_api
    def send(self, message, preview=True, reply_to=None, syntax=None,
             extra=None, attach=None, notify=True):
        """Send a message"""
        args = self._get_call_args(reply_to, extra, attach, notify)
        args["text"] = message
        args["disable_web_page_preview"] = not preview

        syntax = syntaxes.guess_syntax(message, syntax)
        if syntax is not None:
            args["parse_mode"] = syntax

        return self._api.call("sendMessage", args, expect=_objects().Message)

    @_require_api
    def send_photo(self, path=None, file_id=None, url=None, caption=None,
                   syntax=None, reply_to=None, extra=None, attach=None,
                   notify=True):
        """Send a photo"""
        args = self._get_call_args(reply_to, extra, attach, notify)
        if caption is not None:
            args["caption"] = caption
            if syntax is not None:
                syntax = syntaxes.guess_syntax(caption, syntax)
                args["parse_mode"] = syntax
        files = dict()
        args["photo"], files["photo"] = self._get_file_args(path,
                                                            file_id,
                                                            url)
        if files["photo"] is None:
            del files["photo"]

        return self._api.call("sendPhoto", args, files,
                              expect=_objects().Message)

    @_require_api
    def send_audio(self, path=None, file_id=None, url=None, duration=None,
                   thumb=None, performer=None, title=None, reply_to=None,
                   extra=None, attach=None, notify=True, caption=None, *,
                   syntax=None):
        """Send an audio track"""
        args = self._get_call_args(reply_to, extra, attach, notify)
        if caption is not None:
            args["caption"] = caption
            if syntax is not None:
                syntax = syntaxes.guess_syntax(caption, syntax)
                args["parse_mode"] = syntax
        if duration is not None:
            args["duration"] = duration
        if performer is not None:
            args["performer"] = performer
        if title is not None:
            args["title"] = title

        files = dict()
        args["audio"], files["audio"] = self._get_file_args(path,
                                                            file_id,
                                                            url)
        if files["audio"] is None:
            del files["audio"]
        if thumb is not None:
            files["thumb"] = thumb

        return self._api.call("sendAudio", args, files,
                              expect=_objects().Message)

    @_require_api
    def send_voice(self, path=None, file_id=None, url=None, duration=None,
                   title=None, reply_to=None, extra=None, attach=None,
                   notify=True, caption=None, *, syntax=None):
        """Send a voice message"""
        args = self._get_call_args(reply_to, extra, attach, notify)
        if caption is not None:
            args["caption"] = caption
            if syntax is not None:
                syntax = syntaxes.guess_syntax(caption, syntax)
                args["parse_mode"] = syntax
        if duration is not None:
            args["duration"] = duration
        if title is not None:
            args["title"] = title
        syntax = syntaxes.guess_syntax(caption, syntax)
        if syntax is not None:
            args["parse_mode"] = syntax

        files = dict()
        args["voice"], files["voice"] = self._get_file_args(path,
                                                            file_id,
                                                            url)
        if files["voice"] is None:
            del files["voice"]

        return self._api.call("sendVoice", args, files,
                              expect=_objects().Message)

    @_require_api
    def send_video(self, path=None, file_id=None, url=None,
                   duration=None, caption=None, streaming=True, thumb=None,
                   reply_to=None, extra=None, attach=None,
                   notify=True, *, syntax=None):
        """Send a video"""
        args = self._get_call_args(reply_to, extra, attach, notify)
        args["supports_streaming"] = streaming
        if duration is not None:
            args["duration"] = duration
        if caption is not None:
            args["caption"] = caption
            if syntax is not None:
                syntax = syntaxes.guess_syntax(caption, syntax)
                args["parse_mode"] = syntax

        files = dict()
        args["video"], files["video"] = self._get_file_args(path,
                                                            file_id,
                                                            url)
        if files["video"] is None:
            del files["video"]
        if thumb is not None:
            files["thumb"] = thumb

        return self._api.call("sendVideo", args, files,
                              expect=_objects().Message)

    @_require_api
    def send_video_note(self, path=None, file_id=None, duration=None,
                        diameter=None, thumb=None, reply_to=None, extra=None,
                        attach=None, notify=True):
        """Send a video note"""
        args = self._get_call_args(reply_to, extra, attach, notify)
        if duration is not None:
            args["duration"] = duration
        if diameter is not None:
            args["length"] = diameter

        files = dict()
        args["video_note"], files["video_note"] = self._get_file_args(path,
                                                                      file_id,
                                                                      None)
        if files["video_note"] is None:
            del files["video_note"]
        if thumb is not None:
            files["thumb"] = thumb

        return self._api.call("sendVideoNote", args, files,
                              expect=_objects().Message)

    @_require_api
    def send_gif(self, path=None, file_id=None, url=None, duration=None,
                 width=None, height=None, caption=None, thumb=None,
                 reply_to=None, extra=None, attach=None,
                 notify=True, syntax=None):
        """Send an animation"""
        args = self._get_call_args(reply_to, extra, attach, notify)
        if duration is not None:
            args["duration"] = duration
        if caption is not None:
            args["caption"] = caption
            if syntax is not None:
                syntax = syntaxes.guess_syntax(caption, syntax)
                args["parse_mode"] = syntax
        if width is not None:
            args["width"] = width
        if height is not None:
            args["height"] = height

        files = dict()
        args["animation"], files["animation"] = self._get_file_args(path,
                                                                    file_id,
                                                                    url)
        if files["animation"] is None:
            del files["animation"]
        if thumb is not None:
            files["thumb"] = thumb

        return self._api.call("sendAnimation", args, files,
                              expect=_objects().Message)

    @_require_api
    def send_file(self, path=None, file_id=None, url=None, thumb=None,
                  reply_to=None, extra=None, attach=None,
                  notify=True, caption=None, *, syntax=None):
        """Send a generic file"""
        args = self._get_call_args(reply_to, extra, attach, notify)
        if caption is not None:
            args["caption"] = caption
            if syntax is not None:
                syntax = syntaxes.guess_syntax(caption, syntax)
                args["parse_mode"] = syntax

        files = dict()
        args["document"], files["document"] = self._get_file_args(path,
                                                                  file_id,
                                                                  url)
        if files["document"] is None:
            del files["document"]
        if thumb is not None:
            files["thumb"] = thumb

        return self._api.call("sendDocument", args, files,
                              expect=_objects().Message)

    @_require_api
    def send_location(self, latitude, longitude, live_period=None,
                      reply_to=None, extra=None, attach=None, notify=True):
        """Send a geographic location, set live_period to a number between 60
        and 86400 if it's a live location"""
        args = self._get_call_args(reply_to, extra, attach, notify)
        args["latitude"] = latitude
        args["longitude"] = longitude

        if live_period:
            if live_period < 60 or live_period > 86400:
                raise ValueError(
                    "live_period must be a number between 60 and 86400")
            args["live_period"] = live_period

        return self._api.call("sendLocation", args,
                              expect=_objects().Message)

    @_require_api
    def send_venue(self, latitude, longitude, title, address, foursquare=None,
                   reply_to=None, extra=None, attach=None, notify=True):
        """Send a venue"""
        args = self._get_call_args(reply_to, extra, attach, notify)
        args["latitude"] = latitude
        args["longitude"] = longitude
        args["title"] = title
        args["address"] = address
        if foursquare is not None:
            args["foursquare_id"] = foursquare

        self._api.call("sendVenue", args, expect=_objects().Message)

    @_require_api
    def send_sticker(self, sticker=None, reply_to=None, extra=None,
                     attach=None, notify=True, *,
                     path=None, file_id=None, url=None):
        """Send a sticker"""
        if sticker is not None:
            if path is not None:
                raise TypeError("The sticker argument is overridden by " +
                                "the path one")
            path = sticker
            _deprecated_message(
                "The sticker parameter", "1.0", "use the path parameter", -3
            )

        args = self._get_call_args(reply_to, extra, attach, notify)

        files = dict()
        args["sticker"], files["sticker"] = self._get_file_args(path,
                                                                file_id,
                                                                url)
        if files["sticker"] is None:
            del files["sticker"]

        return self._api.call("sendSticker", args, files,
                              expect=_objects().Message)

    @_require_api
    def send_contact(self, phone, first_name, last_name=None, *, reply_to=None,
                     extra=None, attach=None, notify=True):
        """Send a contact"""
        args = self._get_call_args(reply_to, extra, attach, notify)
        args["phone_number"] = phone
        args["first_name"] = first_name

        if last_name is not None:
            args["last_name"] = last_name

        return self._api.call("sendContact", args, expect=_objects().Message)

    @_require_api
    def send_poll(self, question, *kargs, reply_to=None, extra=None,
                  attach=None, notify=True):
        """Send a poll"""
        args = self._get_call_args(reply_to, extra, attach, notify)
        args["question"] = question
        args["options"] = json.dumps(list(kargs))

        return self._api.call("sendPoll", args, expect=_objects().Message)

    @_require_api
    def delete_message(self, message):
        """Delete a message from chat"""
        if hasattr(message, "message_id"):
            message = message.message_id

        return self._api.call("deleteMessage", {
            "chat_id": self.id,
            "message_id": message,
        })

    @_require_api
    def set_photo(self, path):
        """Set a new chat photo"""
        args = {"chat_id": self.id}
        files = {"photo": open(path, "rb")}
        self._api.call("setChatPhoto", args, files)

    @_require_api
    def remove_photo(self):
        """Remove the current chat photo"""
        args = {"chat_id": self.id}
        self._api.call("deleteChatPhoto", args)

    @_require_api
    def send_album(self, album=None, reply_to=None, notify=True):
        """Send a Album"""
        albums = SendAlbum(self, reply_to, notify)
        if album is not None:
            albums._content = album._content
            albums._file = album._file
            albums._used = True
            return albums.send()
        return albums


class MessageMixin:
    """Add some methods for messages"""

    @_require_api
    def forward_to(self, to, notify=True):
        """Forward the message to another user"""
        if hasattr(to, "id"):
            to = to.id

        args = dict()
        args["chat_id"] = to
        args["from_chat_id"] = self.chat.id
        args["message_id"] = self.message_id
        if not notify:
            args["disable_notification"] = True

        return self._api.call("forwardMessage", args,
                              expect=_objects().Message)

    @_require_api
    def edit(self, text, syntax=None, preview=True, extra=None, attach=None):
        """Edit this message"""
        args = {"message_id": self.id, "chat_id": self.chat.id}
        args["text"] = text

        syntax = syntaxes.guess_syntax(text, syntax)
        if syntax is not None:
            args["parse_mode"] = syntax

        if not preview:
            args["disable_web_page_preview"] = True

        if extra is not None:
            _deprecated_message(
                "The extra parameter", "1.0", "use the attach parameter", -3
            )
            args["reply_markup"] = json.dumps(extra.serialize())
        if attach is not None:
            if not hasattr(attach, "_serialize_attachment"):
                raise ValueError("%s is not an attachment" % attach)
            args["reply_markup"] = json.dumps(attach._serialize_attachment(
                self.chat
            ))

        self._api.call("editMessageText", args)
        self.text = text

    @_require_api
    def edit_caption(self, caption, extra=None, attach=None, *, syntax=None):
        """Edit this message's caption"""
        args = {"message_id": self.id, "chat_id": self.chat.id}
        args["caption"] = caption
        syntax = syntaxes.guess_syntax(caption, syntax)
        if syntax is not None:
            args["parse_mode"] = syntax

        if extra is not None:
            _deprecated_message(
                "The extra parameter", "1.0", "use the attach parameter", -3
            )
            args["reply_markup"] = json.dumps(extra.serialize())
        if attach is not None:
            if not hasattr(attach, "_serialize_attachment"):
                raise ValueError("%s is not an attachment" % attach)
            args["reply_markup"] = json.dumps(attach._serialize_attachment(
                self.chat
            ))

        self._api.call("editMessageCaption", args)
        self.caption = caption

    @_require_api
    def edit_attach(self, attach):
        """Edit this message's attachment"""
        args = {"message_id": self.id, "chat_id": self.chat.id}
        if not hasattr(attach, "_serialize_attachment"):
            raise ValueError("%s is not an attachment" % attach)
        args["reply_markup"] = json.dumps(attach._serialize_attachment(
            self.chat
        ))

        self._api.call("editMessageReplyMarkup", args)

    @_require_api
    def edit_live_location(self, latitude, longitude, extra=None, attach=None):
        """Edit this message's live location position"""
        args = {"message_id": self.id, "chat_id": self.chat.id}
        args["latitude"] = latitude
        args["longitude"] = longitude

        if extra is not None:
            _deprecated_message(
                "The extra parameter", "1.0", "use the attach parameter", -3
            )
            args["reply_markup"] = json.dumps(extra.serialize())

        if attach is not None:
            if not hasattr(attach, "_serialize_attachment"):
                raise ValueError("%s is not an attachment" % attach)
            args["reply_markup"] = json.dumps(attach._serialize_attachment(
                self.chat
            ))

        self._api.call("editMessageLiveLocation", args)

    @_require_api
    def stop_live_location(self, extra=None, attach=None):
        """Stop this message's live location"""
        args = {"message_id": self.id, "chat_id": self.chat.id}

        if extra is not None:
            _deprecated_message(
                "The extra parameter", "1.0", "use the attach parameter", -3
            )
            args["reply_markup"] = json.dumps(extra.serialize())

        if attach is not None:
            if not hasattr(attach, "_serialize_attachment"):
                raise ValueError("%s is not an attachment" % attach)
            args["reply_markup"] = json.dumps(attach._serialize_attachment(
                self.chat
            ))
        self._api.call("stopMessageLiveLocation", args)

    @_require_api
    def reply(self, *args, **kwargs):
        """Reply to the current message"""
        return self.chat.send(*args, reply_to=self, **kwargs)

    @_require_api
    def reply_with_photo(self, *args, **kwargs):
        """Reply with a photo to the current message"""
        return self.chat.send_photo(*args, reply_to=self, **kwargs)

    @_require_api
    def reply_with_audio(self, *args, **kwargs):
        """Reply with an audio track to the current message"""
        return self.chat.send_audio(*args, reply_to=self, **kwargs)

    @_require_api
    def reply_with_voice(self, *args, **kwargs):
        """Reply with a voice message to the current message"""
        return self.chat.send_voice(*args, reply_to=self, **kwargs)

    @_require_api
    def reply_with_video(self, *args, **kwargs):
        """Reply with a video to the current message"""
        return self.chat.send_video(*args, reply_to=self, **kwargs)

    @_require_api
    def reply_with_video_note(self, *args, **kwargs):
        """Reply with a video note to the current message"""
        return self.chat.send_video_note(*args, reply_to=self, **kwargs)

    @_require_api
    def reply_with_gif(self, *args, **kwargs):
        return self.chat.send_gif(*args, reply_to=self, **kwargs)

    @_require_api
    def reply_with_file(self, *args, **kwargs):
        """Reply with a generic file to the current chat"""
        return self.chat.send_file(*args, reply_to=self, **kwargs)

    @_require_api
    def reply_with_location(self, *args, **kwargs):
        """Reply with a geographic location to the current chat"""
        return self.chat.send_location(*args, reply_to=self, **kwargs)

    @_require_api
    def reply_with_venue(self, *args, **kwargs):
        """Reply with a venue to the current message"""
        return self.chat.send_venue(*args, reply_to=self, **kwargs)

    @_require_api
    def reply_with_sticker(self, *args, **kwargs):
        """Reply with a sticker to the current message"""
        return self.chat.send_sticker(*args, reply_to=self, **kwargs)

    @_require_api
    def reply_with_contact(self, *args, **kwargs):
        """Reply with a contact to the current message"""
        return self.chat.send_contact(*args, reply_to=self, **kwargs)

    @_require_api
    def reply_with_album(self, *args, **kwargs):
        """Reply with an album to the current message"""
        return self.chat.send_album(*args, reply_to=self, **kwargs)

    @_require_api
    def reply_with_poll(self, *args, **kwargs):
        """Reply with a poll to the current message"""
        return self.chat.send_poll(*args, reply_to=self, **kwargs)

    @_require_api
    def delete(self):
        """Delete the message"""
        return self._api.call("deleteMessage", {
            "chat_id": self.chat.id,
            "message_id": self.id,
        })

    @_require_api
    def stop_poll(self, extra=None, attach=None):
        """Stops a poll"""
        args = dict()
        args["chat_id"] = self.chat.id
        args["message_id"] = self.id

        if extra is not None:
            _deprecated_message(
                "The extra parameter", "1.0", "use the attach parameter", -3
            )
            args["reply_markup"] = json.dumps(extra.serialize())
        if attach is not None:
            if not hasattr(attach, "_serialize_attachment"):
                raise ValueError("%s is not an attachment" % attach)
            args["reply_markup"] = json.dumps(attach._serialize_attachment(
                self.chat
            ))
        return self._api.call("stopPoll", args,
                              expect=_objects().Poll)


class FileMixin:
    """Add some methods for files"""

    @_require_api
    def save(self, path):
        """Save the file to a particular path"""
        response = self._api.call("getFile", {"file_id": self.file_id})

        # Save the file to the wanted path
        downloaded = self._api.file_content(response["result"]["file_path"])
        with open(path, 'wb') as f:
            f.write(downloaded)


class Album:
    """Factory for albums"""
    def __init__(self):
        self._content = []
        self._file = []

    def add_photo(self, path=None, url=None, file_id=None, caption=None,
                  syntax=None):
        """Add a photo the the album instance"""
        args = {"type": "photo"}
        if caption is not None:
            args["caption"] = caption
            if syntax is not None:
                syntax = syntaxes.guess_syntax(caption, syntax)
                args["parse_mode"] = syntax
        if path is not None and file_id is None and url is None:
            name = "photo" + str(len(self._file))
            args["media"] = "attach://" + name
            self._file.append((name, (path, open(path, "rb"))))
        elif file_id is not None and path is None and url is None:
            args["media"] = file_id
        elif url is not None and file_id is None and path is None:
            args["media"] = url
        elif path is None and file_id is None and url is None:
            raise TypeError("path or file_id or URL is missing")
        else:
            raise TypeError("Only one among path, file_id and URL must be" +
                            "passed")

        self._content.append(args)

    def add_video(self, path=None, file_id=None, url=None, duration=None,
                  caption=None, syntax=None):
        """Add a video the the album instance"""
        args = {"type": "video"}
        if duration is not None:
            args["duration"] = duration
        if caption is not None:
            args["caption"] = caption
            if syntax is not None:
                syntax = syntaxes.guess_syntax(caption, syntax)
                args["parse_mode"] = syntax
        if path is not None and file_id is None and url is None:
            name = "photo" + str(len(self._file))
            args["media"] = "attach://" + name
            self._file.append((name, (path, open(path, "rb"))))
        elif file_id is not None and path is None and url is None:
            args["media"] = file_id
        elif url is not None and file_id is None and path is None:
            args["media"] = url
        elif path is None and file_id is None and url is None:
            raise TypeError("path or file_id or URL is missing")
        else:
            raise TypeError("Only one among path, file_id and URL must be" +
                            "passed")

        self._content.append(args)


class SendAlbum(Album):
    """Send the album instance to the chat passed as argument"""
    def __init__(self, chat, reply_to=None, notify=True):
        super(SendAlbum, self).__init__()
        self._get_call_args = chat._get_call_args
        self._api = chat._api
        self.reply_to = reply_to
        self.notify = notify
        self._used = False

    def __enter__(self):
        self._used = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.send()

    def send(self):
        """Send the Album to telgram"""
        args = self._get_call_args(self.reply_to, None, None, self.notify)
        args["media"] = json.dumps(self._content)
        return self._api.call("sendMediaGroup", args, self._file,
                              expect=multiple(_objects().Message))

    def __del__(self):
        if not self._used:
            utils.warn(1, "error_with_album",
                       "you should use `with` to use send_album\
                        -- check the documentation")
