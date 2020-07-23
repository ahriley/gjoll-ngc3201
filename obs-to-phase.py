from astropy.time import Time

targets = ['gjoll_4', 'gjoll_5']
periods = [0.5687630691850727, 0.5514245773501661]
t0s = [1717.0683591970514, 1712.462682561468]

tpars = {'format': 'iso', 'scale': 'utc'}
obs4 = Time(['2019-11-15 07:49:19.17', '2019-11-15 08:31:00.68',
             '2019-11-15 09:12:42.30', '2020-01-18 03:27:17.60',
             '2020-01-18 03:59:21.82'], **tpars)
obs5 = Time(['2019-12-15 05:33:07.20', '2020-02-09 01:37:58.98',
             '2020-02-09 01:54:57.06', '2020-02-09 02:11:41.39',
             '2020-02-09 02:28:21.96', '2020-02-09 02:45:04.28',
             '2020-02-09 03:01:46.63', '2020-02-09 03:18:29.17',
             '2020-02-09 03:35:11.50'], **tpars)
obs = [obs4, obs5]

for target, period, t0, ob in zip(targets, periods, t0s, obs):
    print(target)
    t0_abs = t0 + 2455197.5
    phase = ((ob.to_value('jd') - t0_abs) % period)/period
    for o, p in zip(ob, phase):
        print(o, "{0:.3f}".format(p))
    print()
