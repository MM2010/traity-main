# -*- coding: utf-8 -*-

"""
UserSettings.py
Sistema di impostazioni personalizzate per l'utente.
Gestisce preferenze, configurazioni e profili utente.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
import json
import os
from pathlib import Path

from CONST.constants import AppConstants


@dataclass
class UserProfile:
    """Profilo utente con informazioni personali"""
    profile_id: str
    username: str
    display_name: str
    avatar_emoji: str = "👤"
    created_at: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        """Converte in dizionario per serializzazione"""
        return {
            "profile_id": self.profile_id,
            "username": self.username,
            "display_name": self.display_name,
            "avatar_emoji": self.avatar_emoji,
            "created_at": self.created_at.isoformat(),
            "last_active": self.last_active.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'UserProfile':
        """Crea da dizionario"""
        return cls(
            profile_id=data["profile_id"],
            username=data["username"],
            display_name=data["display_name"],
            avatar_emoji=data.get("avatar_emoji", "👤"),
            created_at=datetime.fromisoformat(data["created_at"]),
            last_active=datetime.fromisoformat(data["last_active"])
        )


@dataclass
class GamePreferences:
    """Preferenze di gioco"""
    default_language: str = "it"
    default_difficulty: str = "medium"
    default_question_type: str = "multiple"
    default_category_id: Optional[int] = None
    questions_per_session: int = 10
    time_limit_per_question: int = 30  # secondi
    show_timer: bool = True
    auto_advance: bool = False
    sound_enabled: bool = True
    vibration_enabled: bool = False  # per dispositivi mobili futuri
    show_hints: bool = True
    show_statistics: bool = True

    def to_dict(self) -> Dict:
        """Converte in dizionario"""
        return {
            "default_language": self.default_language,
            "default_difficulty": self.default_difficulty,
            "default_question_type": self.default_question_type,
            "default_category_id": self.default_category_id,
            "questions_per_session": self.questions_per_session,
            "time_limit_per_question": self.time_limit_per_question,
            "show_timer": self.show_timer,
            "auto_advance": self.auto_advance,
            "sound_enabled": self.sound_enabled,
            "vibration_enabled": self.vibration_enabled,
            "show_hints": self.show_hints,
            "show_statistics": self.show_statistics
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'GamePreferences':
        """Crea da dizionario"""
        return cls(
            default_language=data.get("default_language", "it"),
            default_difficulty=data.get("default_difficulty", "medium"),
            default_question_type=data.get("default_question_type", "multiple"),
            default_category_id=data.get("default_category_id"),
            questions_per_session=data.get("questions_per_session", 10),
            time_limit_per_question=data.get("time_limit_per_question", 30),
            show_timer=data.get("show_timer", True),
            auto_advance=data.get("auto_advance", False),
            sound_enabled=data.get("sound_enabled", True),
            vibration_enabled=data.get("vibration_enabled", False),
            show_hints=data.get("show_hints", True),
            show_statistics=data.get("show_statistics", True)
        )


@dataclass
class NotificationSettings:
    """Impostazioni delle notifiche"""
    achievement_unlocked: bool = True
    daily_reminder: bool = False
    weekly_summary: bool = True
    multiplayer_invites: bool = True
    friend_activity: bool = False
    sound_notifications: bool = True

    def to_dict(self) -> Dict:
        """Converte in dizionario"""
        return {
            "achievement_unlocked": self.achievement_unlocked,
            "daily_reminder": self.daily_reminder,
            "weekly_summary": self.weekly_summary,
            "multiplayer_invites": self.multiplayer_invites,
            "friend_activity": self.friend_activity,
            "sound_notifications": self.sound_notifications
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'NotificationSettings':
        """Crea da dizionario"""
        return cls(
            achievement_unlocked=data.get("achievement_unlocked", True),
            daily_reminder=data.get("daily_reminder", False),
            weekly_summary=data.get("weekly_summary", True),
            multiplayer_invites=data.get("multiplayer_invites", True),
            friend_activity=data.get("friend_activity", False),
            sound_notifications=data.get("sound_notifications", True)
        )


@dataclass
class PrivacySettings:
    """Impostazioni privacy"""
    share_statistics_publicly: bool = False
    allow_friend_requests: bool = True
    show_online_status: bool = True
    share_achievements: bool = True
    collect_usage_data: bool = False
    allow_personalized_ads: bool = False

    def to_dict(self) -> Dict:
        """Converte in dizionario"""
        return {
            "share_statistics_publicly": self.share_statistics_publicly,
            "allow_friend_requests": self.allow_friend_requests,
            "show_online_status": self.show_online_status,
            "share_achievements": self.share_achievements,
            "collect_usage_data": self.collect_usage_data,
            "allow_personalized_ads": self.allow_personalized_ads
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'PrivacySettings':
        """Crea da dizionario"""
        return cls(
            share_statistics_publicly=data.get("share_statistics_publicly", False),
            allow_friend_requests=data.get("allow_friend_requests", True),
            show_online_status=data.get("show_online_status", True),
            share_achievements=data.get("share_achievements", True),
            collect_usage_data=data.get("collect_usage_data", False),
            allow_personalized_ads=data.get("allow_personalized_ads", False)
        )


@dataclass
class UserSettings:
    """Impostazioni complete dell'utente"""
    profile: UserProfile
    game_preferences: GamePreferences = field(default_factory=GamePreferences)
    notification_settings: NotificationSettings = field(default_factory=NotificationSettings)
    privacy_settings: PrivacySettings = field(default_factory=PrivacySettings)
    custom_themes: Dict[str, Dict] = field(default_factory=dict)
    last_modified: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        """Converte in dizionario per serializzazione"""
        return {
            "profile": self.profile.to_dict(),
            "game_preferences": self.game_preferences.to_dict(),
            "notification_settings": self.notification_settings.to_dict(),
            "privacy_settings": self.privacy_settings.to_dict(),
            "custom_themes": self.custom_themes,
            "last_modified": self.last_modified.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'UserSettings':
        """Crea da dizionario"""
        return cls(
            profile=UserProfile.from_dict(data["profile"]),
            game_preferences=GamePreferences.from_dict(data.get("game_preferences", {})),
            notification_settings=NotificationSettings.from_dict(data.get("notification_settings", {})),
            privacy_settings=PrivacySettings.from_dict(data.get("privacy_settings", {})),
            custom_themes=data.get("custom_themes", {}),
            last_modified=datetime.fromisoformat(data["last_modified"])
        )


class SettingsManager:
    """
    Gestore delle impostazioni utente.
    Gestisce caricamento, salvataggio e applicazione delle impostazioni.
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.settings_file = self.data_dir / "user_settings.json"

        # Carica o crea impostazioni di default
        self.current_settings = self._load_settings()

        # Callback per notifiche di cambiamento
        self.on_settings_changed: Optional[callable] = None

    def _load_settings(self) -> UserSettings:
        """Carica le impostazioni dal file"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return UserSettings.from_dict(data)
            except Exception as e:
                print(f"Errore nel caricamento delle impostazioni: {e}")

        # Crea profilo di default
        default_profile = UserProfile(
            profile_id="default",
            username="Player",
            display_name="Giocatore"
        )
        return UserSettings(profile=default_profile)

    def _save_settings(self):
        """Salva le impostazioni nel file"""
        try:
            self.current_settings.last_modified = datetime.now()
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.current_settings.to_dict(), f, indent=2, ensure_ascii=False)

            # Notifica cambiamento
            if self.on_settings_changed:
                self.on_settings_changed(self.current_settings)

        except Exception as e:
            print(f"Errore nel salvataggio delle impostazioni: {e}")

    def get_settings(self) -> UserSettings:
        """Ottiene le impostazioni correnti"""
        return self.current_settings

    def update_profile(self, **kwargs):
        """Aggiorna il profilo utente"""
        for key, value in kwargs.items():
            if hasattr(self.current_settings.profile, key):
                setattr(self.current_settings.profile, key, value)
        self.current_settings.profile.last_active = datetime.now()
        self._save_settings()

    def update_game_preferences(self, **kwargs):
        """Aggiorna le preferenze di gioco"""
        for key, value in kwargs.items():
            if hasattr(self.current_settings.game_preferences, key):
                setattr(self.current_settings.game_preferences, key, value)
        self._save_settings()

    def update_notification_settings(self, **kwargs):
        """Aggiorna le impostazioni delle notifiche"""
        for key, value in kwargs.items():
            if hasattr(self.current_settings.notification_settings, key):
                setattr(self.current_settings.notification_settings, key, value)
        self._save_settings()

    def update_privacy_settings(self, **kwargs):
        """Aggiorna le impostazioni privacy"""
        for key, value in kwargs.items():
            if hasattr(self.current_settings.privacy_settings, key):
                setattr(self.current_settings.privacy_settings, key, value)
        self._save_settings()

    def add_custom_theme(self, theme_name: str, theme_data: Dict):
        """Aggiunge un tema personalizzato"""
        self.current_settings.custom_themes[theme_name] = theme_data
        self._save_settings()

    def remove_custom_theme(self, theme_name: str):
        """Rimuove un tema personalizzato"""
        if theme_name in self.current_settings.custom_themes:
            del self.current_settings.custom_themes[theme_name]
            self._save_settings()

    def get_custom_themes(self) -> Dict[str, Dict]:
        """Ottiene tutti i temi personalizzati"""
        return self.current_settings.custom_themes.copy()

    def reset_to_defaults(self):
        """Resetta tutte le impostazioni ai valori di default"""
        default_profile = UserProfile(
            profile_id=self.current_settings.profile.profile_id,
            username=self.current_settings.profile.username,
            display_name=self.current_settings.profile.display_name,
            avatar_emoji=self.current_settings.profile.avatar_emoji
        )

        self.current_settings = UserSettings(profile=default_profile)
        self._save_settings()

    def export_settings(self, file_path: str):
        """Esporta le impostazioni in un file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.current_settings.to_dict(), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Errore nell'esportazione delle impostazioni: {e}")
            return False

    def import_settings(self, file_path: str) -> bool:
        """Importa le impostazioni da un file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                imported_settings = UserSettings.from_dict(data)

                # Mantieni l'ID del profilo corrente
                imported_settings.profile.profile_id = self.current_settings.profile.profile_id

                self.current_settings = imported_settings
                self._save_settings()
                return True
        except Exception as e:
            print(f"Errore nell'importazione delle impostazioni: {e}")
            return False

    def get_preference(self, category: str, key: str, default: Any = None) -> Any:
        """Ottiene una preferenza specifica"""
        settings_obj = getattr(self.current_settings, category, None)
        if settings_obj and hasattr(settings_obj, key):
            return getattr(settings_obj, key)
        return default

    def set_preference(self, category: str, key: str, value: Any):
        """Imposta una preferenza specifica"""
        settings_obj = getattr(self.current_settings, category, None)
        if settings_obj and hasattr(settings_obj, key):
            setattr(settings_obj, key, value)
            self._save_settings()
