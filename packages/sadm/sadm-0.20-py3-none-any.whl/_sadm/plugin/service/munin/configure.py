# Copyright (c) Jeremías Casteglione <jrmsdev@gmail.com>
# See LICENSE file.

__all__ = ['configure']

def configure(env, cfg):
	env.settings.merge(cfg, 'service.munin', (
		'config.dir',
		'db.dir',
		'dbdir.user',
		'dbdir.group',
	))
