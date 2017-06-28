from datetime import date, timedelta

from api.management.core.database import Database
from .base import Base


class WebuserStatistic(Base):
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, type, period_start=None, period_end=None):
		""" Return all user statistics

		:param type: type of data
		:param period_start: TIMESTAMP
		:param period_end: TIMESTAMP
		"""
		if period_start is None:
			period_end = date.today()
			period_start = period_end - timedelta(days=30)

		if type == 'connectionByDate':
			return {
				'data': self.connection_by_date(period_start, period_end)
			}
		elif type == 'requestByTable':
			return {
				'data': self.request_by_table(period_start, period_end)
			}

		return {
			'error': 'Unknown type of data "%s"' % type
		}

	def connection_by_date(self, period_start, period_end):
		with Database() as db:
			return db.execute("""SELECT count(token.created_on) AS total, to_char(token.created_on, 'YYYY/MM/DD') AS days
								FROM tbl_access_token token
								WHERE token.created_on>=%s AND token.created_on<%s
								GROUP BY days
								ORDER BY days;""", (period_start, period_end))

	def request_by_table(self, period_start, period_end):
		with Database() as db:
			return db.execute("""SELECT
							  count(aa.action_time) AS total,
							  count(aaget.action_time) as get,
							  count(aaput.action_time) as put,
							  count(aapost.action_time) as post,
							  count(aadelete.action_time) as delete,
							  aa.action_object AS table
							FROM tbl_apis_action aa
							  LEFT JOIN tbl_apis_action aaget ON (aaget.action_time = aa.action_time AND aaget.method = 'GET')
							  LEFT JOIN tbl_apis_action aaput ON (aaput.action_time = aa.action_time AND aaput.method = 'PUT')
							  LEFT JOIN tbl_apis_action aapost ON (aapost.action_time = aa.action_time AND aapost.method = 'POST')
							  LEFT JOIN tbl_apis_action aadelete ON (aadelete.action_time = aa.action_time AND aadelete.method = 'DELETE')
							WHERE aa.action_time >= %s AND aa.action_time < %s
							GROUP BY aa.action_object
							ORDER BY aa.action_object;""", (period_start, period_end))
