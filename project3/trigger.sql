CREATE OR REPLACE FUNCTION updateStatusCount() RETURNS trigger AS $updateStatus$
		DECLARE
			old_status_count integer;
		BEGIN
			SELECT num_updates into old_status_count
			FROM NumberOfStatusUpdates
			WHERE userid = NEW.userid;
		
			IF (TG_OP = 'INSERT') THEN
				IF EXISTS (SELECT user_name from NumberOfStatusUpdates
				    WHERE userid = NEW.userid) THEN
					UPDATE NumberOfStatusUpdates
					SET num_updates = num_updates + 1
					WHERE userid = NEW.userid;
				ELSE
					INSERT INTO NumberOfStatusUpdates
					(userid,status_time,text)
					values(NEW.userid,NEW.name,1);
				END IF;
		
			ELSEIF (TG_OP = 'DELETE' AND old_status_count = 1) THEN
				DELETE FROM NumberOfStatusUpdates
				WHERE userid = NEW.userid;
			ELSE 
				UPDATE NumberOfStatusUpdates
				SET num_updates = num_updates - 1
				WHERE userid = NEW.userid;
			END IF;
		RETURN NEW;
		END;
$updateStatus$ LANGUAGE plpgsql;

CREATE TRIGGER update_num_status AFTER 
INSERT OR DELETE ON Status 
FOR EACH ROW EXECUTE PROCEDURE updateStatusCount();
END;
