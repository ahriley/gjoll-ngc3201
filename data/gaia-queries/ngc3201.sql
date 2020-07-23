SELECT source_id, ra, dec, phot_g_mean_mag AS g, bp_rp
FROM gaiadr2.gaia_source
WHERE 1=CONTAINS(
  POINT('ICRS',ra,dec),
  CIRCLE('ICRS',154.403,-46.412, 1))
AND phot_g_mean_mag>=10.8 AND phot_g_mean_mag<=20
