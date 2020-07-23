SELECT source_id, ra, dec, pmra, pmra_error, pmdec, pmdec_error, parallax, parallax_error, phot_g_mean_mag AS g, bp_rp, astrometric_excess_noise, astrometric_chi2_al, astrometric_n_good_obs_al, phot_bp_rp_excess_factor
FROM gaiadr2.gaia_source
WHERE l > 180 AND l < 275
AND b > -35 AND b < 10
AND pmra > 5 AND pmra < 25
AND pmdec > -25 AND pmdec < 0
AND parallax > -2 AND parallax < 2
AND bp_rp > -1 AND bp_rp < 2
AND phot_g_mean_mag <= 20
