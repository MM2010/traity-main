# Entities ER Diagram

```mermaid
erDiagram
    PLAYER_PROFILE ||--o{ GAME_SESSION : plays
    GAME_SESSION ||--|{ QUESTION_RESULT : contains
    PLAYER_PROFILE {
        string player_id PK
        string player_name
        datetime created_at
        dict stats
        list achievements
    }
    GAME_SESSION {
        string session_id PK
        string player_id FK
        string language
        string difficulty
        string question_type
        int category_id
        string category_name
        datetime start_time
        datetime end_time
        bool session_completed
    }
    QUESTION_RESULT {
        string question_id PK
        string session_id FK
        string category
        int category_id
        string difficulty
        string question_type
        string question_text
        string correct_answer
        string user_answer
        float time_taken
        bool is_correct
        datetime timestamp
    }
    ACHIEVEMENT ||--o{ PLAYER_PROFILE : unlocks
    ACHIEVEMENT {
        string achievement_id PK
        string name
        string description
        string icon_path
        bool unlocked
        datetime unlocked_at
    }
    SETTINGS ||--|| PLAYER_PROFILE : has
    SETTINGS {
        string player_id FK
        string language
        string theme
        bool sound_enabled
        dict custom_settings
    }
```

This ER diagram shows the relationships between the main entities in the Traity quiz system:

- Player profiles track overall game statistics
- Game sessions record individual quiz attempts
- Question results store detailed performance data
- Achievements track player milestones
- Settings manage user preferences
