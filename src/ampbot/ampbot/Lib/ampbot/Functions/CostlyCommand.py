"""CostlyCommand.py"""
from Lib.ampbot import Answers, Logger, Parse
from Lib.Spotify import Search, Playlist, Releases, Track
from Lib.Config import Parser
from telegram.ext.dispatcher import run_async
from telegram import InlineQueryResultArticle, InlineQueryResultAudio, InputTextMessageContent, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, MessageEntity, Bot
from uuid import uuid4
import timeit
import arrow
import re

config = Parser.parse_ini('ampbot.ini')
logger = Logger.ConfigureLogger(__name__)

@run_async
def ProcessInlineQuery(bot, update):
    #start = timeit.timeit()
    query = update.inline_query.query
    inline = list()
    releases = list()
    addInline = inline.append
    addRelease = releases.append
    if len(query) > 0:
        if query == 'new albums':
            message = ''
            local = arrow.utcnow().to('Europe/Berlin')
            newReleases = Releases.newReleases(config, 'DE')
            if len(newReleases['albums']['items']) > 0:
                message += 'New Releases {0}\n\n'.format(local.format('YYYY-MM-DD HH:mm'))
                count = 1
                for album in newReleases['albums']['items']:
                    message += '{0}. [{1}]({2}) by {3}\n'.format(count, album['name'], album['external_urls']['spotify'], album['artists'][0]['name'])
                    addRelease(InlineQueryResultArticle(id=uuid4(),
                            title=Parse.AlbumReleaseInlineTitle(count, album),
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Go to Spotify', url=Parse.AlbumUrl(album))]]),
                            input_message_content=InputTextMessageContent(Parse.AlbumReleaseInlineInputMessage(album), ParseMode.MARKDOWN, False),
                            description=Parse.AlbumInlineDescription(album),
                            thumb_url=Parse.AlbumThumbUrl(album),
                            thumb_width=640,
                            thumb_height=640))
                    count += 1

                addInline(InlineQueryResultArticle(id=uuid4(),
                            title='New Releases {0}\n\n'.format(local.format('YYYY-MM-DD HH:mm')),
                            reply_markup=None,
                            input_message_content=InputTextMessageContent(message, ParseMode.MARKDOWN, True)))
                for release in releases:
                    addInline(release)
        else:
            results = Search.getResults(query, config)
            if len(results['tracks']['items']) > 0:
                for track in results['tracks']['items']:
                    if Parse.TrackPreviewUrl(track) != None:
                        addInline(InlineQueryResultAudio(id='spotify:track:{0}'.format(track['id']), #uuid4(),
                                audio_url=Parse.TrackPreviewUrl(track),
                                performer=Parse.TrackArtists(track),
                                title=Parse.TrackInlineTitle(track),
                                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Go to Spotify', url=Parse.TrackUrl(track))]]),
                                input_message_content=InputTextMessageContent(Parse.TrackInlineInputMessage(track), ParseMode.MARKDOWN, False)))
                    else:
                        addInline(InlineQueryResultArticle(id='spotify:track:{0}'.format(track['id']), #uuid4(),
                            title=Parse.TrackInlineTitleWithOutPreview(track),
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Go to Spotify', url=Parse.TrackUrl(track))]]),
                            input_message_content=InputTextMessageContent(Parse.TrackInlineInputMessage(track), ParseMode.MARKDOWN, False),
                            description=Parse.TrackInlineDescriptionWithOutPreview(track),
                            url=Parse.TrackUrl(track),
                            hide_url=True,
                            thumb_url=Parse.TrackThumbUrl(track),
                            thumb_width=640,
                            thumb_height=640))                
            if len(results['artists']['items']) > 0:
                for artist in results['artists']['items']:
                    addInline(InlineQueryResultArticle(id=uuid4(),
                            title=Parse.ArtistInlineTitle(artist),
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Go to Spotify', url=Parse.ArtistUrl(artist))]]),
                            input_message_content=InputTextMessageContent(Parse.ArtistInlineInputMessage(artist), ParseMode.MARKDOWN, False),
                            description=Parse.ArtistInlineDescription(artist),
                            thumb_url=Parse.ArtistThumbUrl(artist),
                            thumb_width=640,
                            thumb_height=640))
            if len(results['albums']['items']) > 0:
                for album in results['albums']['items']:
                    addInline(InlineQueryResultArticle(id=uuid4(),
                            title=Parse.AlbumInlineTitle(album),
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Go to Spotify', url=Parse.AlbumUrl(album))]]),
                            input_message_content=InputTextMessageContent(Parse.AlbumInlineInputMessage(album), ParseMode.MARKDOWN, False),
                            description=Parse.AlbumInlineDescription(album),
                            thumb_url=Parse.AlbumThumbUrl(album),
                            thumb_width=640,
                            thumb_height=640))
            if len(results['playlists']['items']) > 0:
                for playlist in results['playlists']['items']:
                    addInline(InlineQueryResultArticle(id=uuid4(),
                            title=Parse.PlaylistInlineTitle(playlist),
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Go to Spotify', url=Parse.PlaylistUrl(playlist))]]),
                            input_message_content=InputTextMessageContent(Parse.PlaylistInlineInputMessage(playlist), ParseMode.MARKDOWN, False),
                            description=Parse.PlaylistInlineDescription(playlist),
                            thumb_url=Parse.PlaylistThumbUrl(playlist),
                            thumb_width=640,
                            thumb_height=640))
        bot.answerInlineQuery(update.inline_query.id, inline)
        logger.info('INLINE: @{0}({1}): {2}'.format(update.inline_query.from_user.username, update.inline_query.from_user.id, update.inline_query.query))
    elif len(query) == 0 or query == None:
        addInline(InlineQueryResultArticle(id=uuid4(),
                            title='to get the new Releases',
                            description='type in "new albums"',
                            reply_markup=None,
                            input_message_content=InputTextMessageContent('How to use my inline query?\n\nto get the new Releases type in "`new albums`"', parse_mode=ParseMode.MARKDOWN)))
        addInline(InlineQueryResultArticle(id=uuid4(),
                            title='to get the a track/album/artist/playlist',
                            description='type in "track/album/artist/playlist"',
                            reply_markup=None,
                            input_message_content=InputTextMessageContent('How to use my inline query?\n\nto get the a track/album/artist/playlist type in "`track/album/artist/playlist`"', parse_mode=ParseMode.MARKDOWN)))
        bot.answerInlineQuery(update.inline_query.id, inline, switch_pm_text='How to use my inline query?', switch_pm_parameter='help')
        logger.info('INLINE: @{0}({1}): {2}'.format(update.inline_query.from_user.username, update.inline_query.from_user.id, update.inline_query.query))
    else:
        pass
    #end = timeit.timeit()
    #logger.info('running time: {0}'.format(end - start))

@run_async
def ProcessChosenInlineResult(bot, update):
    id = update.chosen_inline_result.result_id
    username = update.chosen_inline_result.from_user.first_name
    if 'spotify:track:' in id:
        if Playlist.addTrack(id, config):
            Playlist.updatePlaylistName(update.chosen_inline_result.from_user.first_name, config)
    logger.info('CHOSEN: @{0}({1})'.format(update.chosen_inline_result.from_user.username, update.chosen_inline_result.from_user.id))

@run_async
def ProcessCallbackQuery(bot, update):
    query = update.callback_query
    logger.info('CALLBACK: @{0}({1})'.format(update.message.from_user.username, update.message.from_user.id))

@run_async
def ProcessNewAlbumReleases(bot, update):
    message = ''
    local = arrow.utcnow().to('Europe/Berlin')
    newReleases = Releases.newReleases(config, 'DE')
    if len(newReleases['albums']['items']) > 0:
        message += 'New Releases {0}\n\n'.format(local.format('YYYY-MM-DD HH:mm'))
        count = 1
        for album in newReleases['albums']['items']:
            message += '{0}. [{1}]({2}) by {3}\n'.format(count, album['name'], album['external_urls']['spotify'], album['artists'][0]['name'])
            count += 1
    bot.sendMessage(update.message.chat_id, message, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    logger.info('NEW: {0}({1})'.format(update.message.from_user.username, update.message.from_user.id))

@run_async
def ProcessAddTrackToPlaylist(bot, update, args, user_data, chat_data):
    if len(args) > 0:
        if 'spotify:track:' in args[0]:
            if Playlist.addTrack(args[0], config):
                update.message.reply_text(Parse.TrackAddedSuccessDescription(Track.getTrackById(args[0], config)))
                Playlist.updatePlaylistName(update.message.from_user.first_name, config)
            else:
                update.message.reply_text(Parse.TrackAddedFailedDescription(Track.getTrackById(args[0], config)))

        if 'https://open.spotify.com/track/' in args[0]:
            id = args[0].replace("https://open.spotify.com/track/", "spotify:track:")
            if Playlist.addTrack(id, config):
                update.message.reply_text(Parse.TrackAddedSuccessDescription(Track.getTrackById(id, config)))
                Playlist.updatePlaylistName(update.message.from_user.first_name, config)
            else:
                update.message.reply_text(Parse.TrackAddedFailedDescription(Track.getTrackById(id, config)))
    elif update.message.reply_to_message != None:
            matches = re.findall(r"spotify:track:[^\s]+", update.message.reply_to_message.text)
            if len(matches) > 0:
                for match in matches:
                    if 'spotify:track:' in match:
                        if Playlist.addTrack(match, config):
                            update.message.reply_text(Parse.TrackAddedSuccessDescription(Track.getTrackById(match, config)))
                            Playlist.updatePlaylistName(update.message.from_user.first_name, config)
                        else:
                            update.message.reply_text(Parse.TrackAddedFailedDescription(Track.getTrackById(match, config)))

            for entity in update.message.reply_to_message.entities:
                if entity.type == MessageEntity.URL:
                    if 'https://open.spotify.com/track/' in update.message.reply_to_message.text[entity.offset:entity.offset + entity.length]:
                        id = update.message.reply_to_message.text[entity.offset:entity.offset + entity.length].replace("https://open.spotify.com/track/", "spotify:track:")
                        if Playlist.addTrack(id, config):
                            update.message.reply_text(Parse.TrackAddedSuccessDescription(Track.getTrackById(id, config)))
                            Playlist.updatePlaylistName(update.message.from_user.first_name, config)
                        else:
                            update.message.reply_text(Parse.TrackAddedFailedDescription(Track.getTrackById(id, config)))
                elif entity.type == MessageEntity.TEXT_LINK:
                    if 'https://open.spotify.com/track/' in entity.url:
                        id = entity.url.replace("https://open.spotify.com/track/", "spotify:track:")
                        if Playlist.addTrack(id, config):
                            update.message.reply_text(Parse.TrackAddedSuccessDescription(Track.getTrackById(id, config)))
                            Playlist.updatePlaylistName(update.message.from_user.first_name, config)
                        else:
                            update.message.reply_text(Parse.TrackAddedFailedDescription(Track.getTrackById(id, config)))
                else:
                    pass