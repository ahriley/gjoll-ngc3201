SELECT source_id, ra, dec, phot_g_mean_mag AS g, bp_rp
FROM gaiadr2.gaia_source
WHERE 1=CONTAINS(
  POINT('ICRS',ra,dec),
  CIRCLE('ICRS',189.867,-26.744, 0.25))
AND phot_g_mean_mag>=11.5 AND phot_g_mean_mag<=20
