from typing import Type, TypeVar, MutableMapping, Any, Iterable, Union
import datetime
import copy

from datapipelines import DataSource, PipelineContext, Query, validate_query

from .. import utctimestamp
from ..data import Platform, Queue
from ..core import Champion, Rune, Item, Map, SummonerSpell, Realms, ProfileIcon, LanguageStrings, Summoner, ChampionMastery, Match, CurrentMatch, ShardStatus, ChallengerLeague, MasterLeague, League, MatchHistory, Items, Champions, Maps, ProfileIcons, Locales, Runes, SummonerSpells, Versions, ChampionMasteries, LeagueEntries, FeaturedMatches, VerificationString
from ..core.match import Timeline, MatchListData
from ..core.championmastery import ChampionMasteryListData
from ..core.league import LeaguePositionsData, LeagueEntry
from ..core.spectator import FeaturedGamesData
from ..core.staticdata.item import ItemListData
from ..core.staticdata.champion import ChampionListData, ChampionData
from ..core.staticdata.map import MapListData
from ..core.staticdata.profileicon import ProfileIconListData
from ..core.staticdata.language import LanguagesData
from ..core.staticdata.rune import RuneListData
from ..core.staticdata.summonerspell import SummonerSpellListData
from ..core.staticdata.version import VersionListData
from .riotapi.staticdata import _get_latest_version, _get_default_locale
from .uniquekeys import convert_region_to_platform

T = TypeVar("T")


class UnloadedGhostStore(DataSource):
    def __init__(self):
        super().__init__()

    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    _validate_get_versions_query = Query. \
        has("platform").as_(Platform)

    _validate_get_realms_query = Query. \
        has("platform").as_(Platform)

    _validate_get_champion_query = Query. \
        has("platform").as_(Platform).also. \
        has("id").as_(int).or_("name").as_(str).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").also. \
        can_have("includedData")

    _validate_get_champions_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"}).also. \
        can_have("dataById").with_default(True)

    _validate_get_rune_query = Query. \
        has("id").as_(int).or_("name").as_(str).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    _validate_get_runes_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    _validate_get_item_query = Query. \
        has("id").as_(int).or_("name").as_(str).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    _validate_get_items_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    _validate_get_map_query = Query. \
        has("id").as_(int).or_("name").as_(str).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str)

    _validate_get_maps_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str)

    _validate_get_summoner_spell_query = Query. \
        has("id").as_(int).or_("name").as_(str).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    _validate_get_summoner_spells_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    _validate_get_languages_query = Query. \
        has("platform").as_(Platform)

    _validate_get_language_strings_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str)

    _validate_get_profile_icon_query = Query. \
        has("platform").as_(Platform).also. \
        has("id").as_(int).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str)

    _validate_get_profile_icons_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str)

    _validate_get_champion_mastery_query = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.id").also. \
        has("champion.id").as_(int)

    _validate_get_champion_masteries_query = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.id").as_(int)

    _validate_get_league_entries_query = Query. \
        has("summoner.id").as_(int).also. \
        has("platform").as_(Platform)

    _validate_get_league_query = Query. \
        has("id").as_(str).also. \
        has("platform").as_(Platform)

    _validate_get_challenger_league_query = Query. \
        has("queue").as_(Queue).also. \
        has("platform").as_(Platform)

    _validate_get_master_league_query = Query. \
        has("queue").as_(Queue).also. \
        has("platform").as_(Platform)

    _validate_get_current_match_query = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.id").as_(int)

    _validate_get_featured_matches_query = Query. \
        has("platform").as_(Platform)

    _validate_get_match_query = Query. \
        has("id").as_(int).also. \
        has("platform").as_(Platform)

    _validate_get_match_history_query = Query. \
        has("account.id").as_(int).also. \
        has("platform").as_(Platform).also. \
        can_have("beginTime").as_(int).also. \
        can_have("endTime").as_(int).also. \
        can_have("beginIndex").as_(int).also. \
        can_have("endIndex").as_(int).also. \
        can_have("seasons").as_(Iterable).also. \
        can_have("champion.ids").as_(Iterable).also. \
        can_have("queues").as_(Iterable)

    _validate_get_timeline_query = Query. \
        has("id").as_(int).also. \
        has("platform").as_(Platform)

    _validate_get_shard_status_query = Query. \
        has("platform").as_(Platform)

    _validate_get_summoner_query = Query. \
        has("id").as_(int). \
        or_("account.id").as_(int). \
        or_("name").as_(str).also. \
        has("platform").as_(Platform)

    _validate_get_verification_string_query = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.id").as_(int)

    @get.register(Champion)
    @validate_query(_validate_get_champion_query, convert_region_to_platform)
    def get_champion(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Champion:
        query["region"] = query.pop("platform").region
        return Champion._construct_normally(**query)

    @get.register(Rune)
    @validate_query(_validate_get_rune_query, convert_region_to_platform)
    def get_rune(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Rune:
        query["region"] = query.pop("platform").region
        query["includedData"] = query.pop("includedData")
        return Rune._construct_normally(**query)

    @get.register(Item)
    @validate_query(_validate_get_item_query, convert_region_to_platform)
    def get_item(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Item:
        query["region"] = query.pop("platform").region
        query["includedData"] = query.pop("includedData")
        return Item._construct_normally(**query)

    @get.register(Map)
    @validate_query(_validate_get_map_query, convert_region_to_platform)
    def get_map(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Map:
        query["region"] = query.pop("platform").region
        return Map._construct_normally(**query)

    @get.register(SummonerSpell)
    @validate_query(_validate_get_summoner_spell_query, convert_region_to_platform)
    def get_summoner_spell(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> SummonerSpell:
        query["region"] = query.pop("platform").region
        query["includedData"] = query.pop("includedData")
        return SummonerSpell._construct_normally(**query)

    @get.register(Realms)
    @validate_query(_validate_get_realms_query, convert_region_to_platform)
    def get_realms(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Realms:
        query["region"] = query.pop("platform").region
        return Realms._construct_normally(**query)

    @get.register(ProfileIcon)
    @validate_query(_validate_get_profile_icon_query, convert_region_to_platform)
    def get_profile_icons(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ProfileIcon:
        query["region"] = query.pop("platform").region
        return ProfileIcon._construct_normally(**query)

    @get.register(LanguageStrings)
    @validate_query(_validate_get_language_strings_query, convert_region_to_platform)
    def get_language_strings(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> LanguageStrings:
        query["region"] = query.pop("platform").region
        return LanguageStrings._construct_normally(**query)

    @get.register(Summoner)
    @validate_query(_validate_get_summoner_query, convert_region_to_platform)
    def get_summoner(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Summoner:
        query["region"] = query.pop("platform").region
        if "account.id" in query:
            query["account"] = query.pop("account.id")
        return Summoner._construct_normally(**query)

    @get.register(ChampionMastery)
    @validate_query(_validate_get_champion_mastery_query, convert_region_to_platform)
    def get_champion_mastery(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionMastery:
        query["region"] = query.pop("platform").region
        if "summoner.id" in query:
            query["summoner"] = query.pop("summoner.id")
        if "summoner.name" in query:
            query["summoner"] = query.pop("summoner.name")
        if "summoner.account.id" in query:
            query["_account_id"] = query.pop("summoner.account.id")
        if "champion.id" in query:
            query["champion"] = query.pop("champion.id")
        if "champion.id" in query:
            query["champion"] = query.pop("champion.name")
        return ChampionMastery._construct_normally(**query)

    @get.register(Match)
    @validate_query(_validate_get_match_query, convert_region_to_platform)
    def get_match(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Match:
        query["region"] = query.pop("platform").region
        return Match._construct_normally(**query)

    @get.register(Timeline)
    @validate_query(_validate_get_timeline_query, convert_region_to_platform)
    def get_match(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Timeline:
        query["region"] = query.pop("platform").region
        return Timeline._construct_normally(**query)

    @get.register(CurrentMatch)
    @validate_query(_validate_get_current_match_query, convert_region_to_platform)
    def get_current_match(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> CurrentMatch:
        query["region"] = query.pop("platform").region
        query["summoner"] = query.pop("summoner.id")
        return CurrentMatch._construct_normally(**query)

    @get.register(ShardStatus)
    @validate_query(_validate_get_shard_status_query, convert_region_to_platform)
    def get_shard_status(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ShardStatus:
        query["region"] = query.pop("platform").region
        return ShardStatus._construct_normally(**query)

    @get.register(ChallengerLeague)
    @validate_query(_validate_get_challenger_league_query, convert_region_to_platform)
    def get_challenger_league(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChallengerLeague:
        UnloadedGhostStore._validate_get_challenger_league_query(query)
        query["region"] = query.pop("platform").region
        return ChallengerLeague._construct_normally(**query)

    @get.register(MasterLeague)
    @validate_query(_validate_get_master_league_query, convert_region_to_platform)
    def get_master_league(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MasterLeague:
        query["region"] = query.pop("platform").region
        return MasterLeague._construct_normally(**query)

    @get.register(League)
    @validate_query(_validate_get_league_query, convert_region_to_platform)
    def get_league(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> League:
        query["region"] = query.pop("platform").region
        query["id"] = query.pop("id")
        return League._construct_normally(**query)

    @get.register(VerificationString)
    @validate_query(_validate_get_verification_string_query, convert_region_to_platform)
    def get_verification_string(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> VerificationString:
        query["region"] = query.pop("platform").region
        query["summoner"] = Summoner(id=query.pop("summoner.id"), region=query["region"])
        return VerificationString._construct_normally(**query)

    @get.register(MatchHistory)
    @validate_query(_validate_get_match_history_query, convert_region_to_platform)
    def get_match_history(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MatchHistory:
        original_query = copy.deepcopy(query)
        region = query["region"]
        account_id = query["account.id"]
        begin_index = query.get("beginIndex", 0)
        end_index = query.get("endIndex", None)
        begin_time = query.get("beginTime", 0)  # Defaults to start of summoner's match history
        end_time = query.get("endTime", None)  # Defaults to now; end_time > begin_time
        queues = query.get("queues", {})
        seasons = query.get("seasons", {})
        champion_ids = query.get("champion.ids", {})

        max_number_of_requested_matches = float("inf") if end_index is None else end_index - begin_index

        # Convert times to datetimes
        begin_time = datetime.datetime.utcfromtimestamp(begin_time / 1000)
        if end_time is not None:
            end_time = datetime.datetime.utcfromtimestamp(end_time / 1000)
            assert end_time > begin_time

        # Create the generator that will populate the match history object.
        def generate_matchlists(begin_index: int, max_number_of_requested_matches: int = None, begin_time: datetime.datetime = None, end_time: Union[datetime.datetime, None] = None):
            _begin_index = begin_index
            _begin_time = begin_time

            if isinstance(max_number_of_requested_matches, int):
                max_number_of_requested_matches = float(max_number_of_requested_matches)

            pulled_matches = 0
            while pulled_matches < max_number_of_requested_matches:
                new_query = {
                    "region": region,
                    "account.id": account_id,
                    "queues": queues,
                    "seasons": seasons,
                    "champion.ids": champion_ids,
                    "beginIndex": _begin_index,
                    "beginTime": int(utctimestamp(_begin_time) * 1000),
                    "maxNumberOfMatches": max_number_of_requested_matches
                }
                if "endTime" in original_query:
                    new_query["endTime"] = original_query["endTime"]

                data = context[context.Keys.PIPELINE].get(MatchListData, query=new_query)
                match = None
                for matchrefdata in data:
                    match = Match.from_match_reference(matchrefdata)
                    pulled_matches += 1
                    if pulled_matches > 0 and (end_time is None or match.creation < end_time) and match.creation > begin_time:
                        yield  match
                    if pulled_matches >= max_number_of_requested_matches:
                        break

                matches_pulled_this_iteration = len(data)
                if hasattr(data, "endIndex"):
                    expected_pulled_matches_this_iteration = data.endIndex - data.beginIndex
                else:
                    expected_pulled_matches_this_iteration = None
                if expected_pulled_matches_this_iteration is not None and matches_pulled_this_iteration < expected_pulled_matches_this_iteration:
                    # Stop because the API returned less data than we asked for, and so there isn't any more left
                    break

                if end_time is not None and match is not None and match.creation >= end_time:
                    # Stop because we have gotten all the matches in the requested time range
                    break

                if hasattr(data, "endIndex"):
                    _begin_index = data.endIndex
                # else: Don't update it
                if hasattr(data, "endTime"):
                    _begin_time = datetime.datetime.utcfromtimestamp(data.endTime / 1000)
                # else: Don't update it
                max_number_of_requested_matches -= len(data)

                if end_time is not None and _begin_time >= end_time:
                    # Stop because we have gotten all the matches in the requested time range
                    break

        generator = generate_matchlists(begin_index, max_number_of_requested_matches, begin_time, end_time)

        generator = MatchHistory.from_generator(generator=generator, account_id=account_id, region=region,
                                                begin_index=begin_index, end_index=end_index,
                                                begin_time=begin_time, end_time=end_time,
                                                queues=queues, seasons=seasons, champions=champion_ids)
        return generator

    @get.register(Items)
    @validate_query(_validate_get_items_query, convert_region_to_platform)
    def get_items(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Items:
        def items_generator(query):
            data = context[context.Keys.PIPELINE].get(ItemListData, query)
            for itemdata in data:
                item = Item.from_data(itemdata)
                yield item
        kwargs = {
            "region": query["region"],
            "version": query["version"],
            "locale": query["locale"],
            "included_data": query["includedData"],
        }
        return Items.from_generator(generator=items_generator(query), **kwargs)

    @get.register(Champions)
    @validate_query(_validate_get_champions_query, convert_region_to_platform)
    def get_champions(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Champions:
        def champions_generator(query):
            data = context[context.Keys.PIPELINE].get(ChampionListData, query)
            for champion_data in data:
                champion = Champion.from_data(champion_data, loaded_groups={ChampionData})
                yield champion
        kwargs = {
            "region": query["region"],
            "version": query["version"],
            "locale": query["locale"],
            "included_data": query["includedData"],
        }
        return Champions.from_generator(generator=champions_generator(query), **kwargs)

    @get.register(Maps)
    @validate_query(_validate_get_maps_query, convert_region_to_platform)
    def get_maps(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Maps:
        def maps_generator(query):
            data = context[context.Keys.PIPELINE].get(MapListData, query)
            for map_data in data:
                map = Map.from_data(map_data)
                yield map
        kwargs = {
            "region": query["region"],
            "version": query["version"],
            "locale": query["locale"]
        }
        return Maps.from_generator(generator=maps_generator(query), **kwargs)

    @get.register(ProfileIcons)
    @validate_query(_validate_get_profile_icons_query, convert_region_to_platform)
    def get_profile_icons(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ProfileIcons:
        def profile_icons_generator(query):
            data = context[context.Keys.PIPELINE].get(ProfileIconListData, query)
            for profile_icon_data in data:
                profile_icon = ProfileIcon.from_data(profile_icon_data)
                yield profile_icon
        kwargs = {
            "region": query["region"],
            "version": query["version"],
            "locale": query["locale"]
        }
        return ProfileIcons.from_generator(generator=profile_icons_generator(query), **kwargs)

    @get.register(Locales)
    @validate_query(_validate_get_languages_query, convert_region_to_platform)
    def get_locales(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Locales:
        def locales_generator(query):
            data = context[context.Keys.PIPELINE].get(LanguagesData, query)
            for locale in data:
                yield locale
        kwargs = {
            "region": query["region"]
        }
        return Locales.from_generator(generator=locales_generator(query), **kwargs)

    @get.register(Runes)
    @validate_query(_validate_get_runes_query, convert_region_to_platform)
    def get_runes(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Runes:
        def runes_generator(query):
            data = context[context.Keys.PIPELINE].get(RuneListData, query)
            for runedata in data:
                rune = Rune.from_data(runedata)
                yield rune
        kwargs = {
            "region": query["region"],
            "version": query["version"],
            "locale": query["locale"],
            "included_data": query["includedData"],
        }
        return Runes.from_generator(generator=runes_generator(query), **kwargs)

    @get.register(SummonerSpells)
    @validate_query(_validate_get_summoner_spells_query, convert_region_to_platform)
    def get_summoner_spells(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> SummonerSpells:
        def summoner_spells_generator(query):
            data = context[context.Keys.PIPELINE].get(SummonerSpellListData, query)
            for summoner_spelldata in data:
                summoner_spell = SummonerSpell.from_data(summoner_spelldata)
                yield summoner_spell
        kwargs = {
            "region": query["region"],
            "version": query["version"],
            "locale": query["locale"],
            "included_data": query["includedData"],
        }
        return SummonerSpells.from_generator(generator=summoner_spells_generator(query), **kwargs)

    @get.register(Versions)
    @validate_query(_validate_get_versions_query, convert_region_to_platform)
    def get_versions(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Versions:
        def versions_generator(query):
            data = context[context.Keys.PIPELINE].get(VersionListData, query)
            for version in data:
                yield version
        kwargs = {
            "region": query["region"]
        }
        return Versions.from_generator(generator=versions_generator(query), **kwargs)

    @get.register(ChampionMasteries)
    @validate_query(_validate_get_champion_masteries_query, convert_region_to_platform)
    def get_versions(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionMasteries:
        def champion_masteries_generator(query):
            from ..transformers.championmastery import ChampionMasteryTransformer
            all_champion_ids = [champion.id for champion in Champions(region=query["region"])]
            data = context[context.Keys.PIPELINE].get(ChampionMasteryListData, query)
            for champion_mastery_data in data:
                champion_mastery = ChampionMastery.from_data(champion_mastery_data)
                all_champion_ids.remove(champion_mastery.champion.id)
                yield champion_mastery
            for unfound_id in all_champion_ids:
                dto = {
                    "championId": unfound_id,
                    "playerId": query["summoner.id"],
                    "championLevel": 0,
                    "chestGranted": False,
                    "championPoints": 0,
                    "championPointsUntilNextLevel": 1800,
                    "championPointsSinceLastLevel": 0,
                    "lastPlayTime": None,
                    "region": query["region"]
                }
                champion_mastery_data = ChampionMasteryTransformer.champion_mastery_dto_to_data(None, dto)
                champion_mastery = ChampionMastery.from_data(champion_mastery_data)
                yield champion_mastery
        kwargs = {
            "region": query["region"],
            "summoner": Summoner(id=query["summoner.id"], region=query["region"])
        }
        return ChampionMasteries.from_generator(generator=champion_masteries_generator(query), **kwargs)

    @get.register(LeagueEntries)
    @validate_query(_validate_get_league_entries_query, convert_region_to_platform)
    def get_league_entries(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> LeagueEntries:
        def league_entries_generator(query):
            data = context[context.Keys.PIPELINE].get(LeaguePositionsData, query)
            for position_data in data:
                position = LeagueEntry.from_data(position_data)
                yield position
        kwargs = {
            "region": query["region"],
            "summoner": Summoner(id=query["summoner.id"], region=query["region"])
        }
        return LeagueEntries.from_generator(generator=league_entries_generator(query), **kwargs)

    @get.register(FeaturedMatches)
    @validate_query(_validate_get_featured_matches_query, convert_region_to_platform)
    def get_featured_matches(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> FeaturedMatches:
        def featured_matches_generator(query):
            data = context[context.Keys.PIPELINE].get(FeaturedGamesData, query)
            for match_data in data:
                match = CurrentMatch.from_data(match_data, summoner=None)
                yield match
        kwargs = {
            "region": query["region"]
        }
        return FeaturedMatches.from_generator(generator=featured_matches_generator(query), **kwargs)