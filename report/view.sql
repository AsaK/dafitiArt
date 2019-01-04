CREATE VIEW IF NOT EXISTS average_work AS
  SELECT id, name, email, avatar, AVG(Diference) / 60 as work_average FROM (
    SELECT user.id, user.name, user.email, user.avatar, strftime('%s', MAX(art.created_at)) - strftime('%s',MIN(art.created_at)) as Diference
      FROM art_artrequestevent as art
      LEFT JOIN core_user as user ON art.user_id == user.id
     WHERE art.event == 'ChangeStatus'
       AND user.type == 3
     GROUP BY art.art_request_id, art.user_id
) as x GROUP BY id

