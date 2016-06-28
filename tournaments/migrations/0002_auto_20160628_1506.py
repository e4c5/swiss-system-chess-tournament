# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-28 12:06
from __future__ import unicode_literals
    
from django.db import migrations, connection


def forwards(apps, schema_editor):
    if connection.vendor == 'mysql':
        query = """
            CREATE VIEW tournaments_tournament_player_score AS
            SELECT CONCAT(tournaments_round.tournament_id, ':', player_score.player_id) as id, 
                tournaments_round.tournament_id, player_score.player_id, SUM(player_score.score) as score,
                player.name, player.rating, player.fide_title,
                case player.fide_title
                    when "GM"  then 8
                    when "IM"  then 7
                    when "WGM" then 6
                    when "FM"  then 5
                    when "WIM" then 4
                    when "CM"  then 3
                    when "WFM" then 2
                    when "WCM" then 1
                    else 0 
                    end as title_number
                
                FROM tournaments_round
                    INNER JOIN tournaments_game_player_score as `player_score` 
                    ON (tournaments_round.id = player_score.round_id)
                    INNER JOIN tournaments_player as `player` 
                    ON (player.id = player_score.player_id)
                GROUP BY tournaments_round.tournament_id, player_score.player_id
            """
    else :
        query = """
            CREATE VIEW tournaments_tournament_player_score AS
            SELECT tournaments_round.tournament_id || ':' || player_score.player_id as id, 
                tournaments_round.tournament_id, player_score.player_id, SUM(player_score.score) as score,
                player.name, player.rating, player.fide_title,
                case player.fide_title
                    when "GM"  then 8
                    when "IM"  then 7
                    when "WGM" then 6
                    when "FM"  then 5
                    when "WIM" then 4
                    when "CM"  then 3
                    when "WFM" then 2
                    when "WCM" then 1
                    else 0 
                    end as title_number
                
                FROM tournaments_round
                    INNER JOIN tournaments_game_player_score as `player_score` 
                    ON (tournaments_round.id = player_score.round_id)
                    INNER JOIN tournaments_player as `player` 
                    ON (player.id = player_score.player_id)
                GROUP BY tournaments_round.tournament_id, player_score.player_id
            """
        connection.cursor().execute(query);

def backwards(apps, schema_editor):
    connection.cursor().execute("""  DROP VIEW tournaments_tournament_player_score; """)


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL("""
            CREATE VIEW tournaments_game_player_score AS
                SELECT id as game_id, round_id, player_id, player_score as score FROM tournaments_game
                UNION ALL
                SELECT id as game_id, round_id, opponent_id as player_id, opponent_score as score
                    FROM tournaments_game
                    WHERE opponent_id IS NOT NULL
            ;
        """, 
        """ DROP VIEW tournaments_game_player_score;"""),
        
        migrations.RunPython(forwards, backwards)
    ]

