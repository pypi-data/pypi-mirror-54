from enum import Enum
import logging
import binascii
from blatann.nrf.nrf_dll_load import driver
import blatann.nrf.nrf_driver_types as util
from blatann.nrf.nrf_types.enums import *
from blatann.nrf.nrf_types.gap import BLEGapAddr


logger = logging.getLogger(__name__)


class BLEGapSecMode(object):
    def __init__(self, sec_mode, level):
        self.sm = sec_mode
        self.level = level

    def to_c(self):
        params = driver.ble_gap_conn_sec_mode_t()
        params.sm = self.sm
        params.lv = self.level
        return params

    @classmethod
    def from_c(cls, params):
        return cls(params.sm, params.lv)


class BLEGapSecModeType(object):
    NO_ACCESS = BLEGapSecMode(0, 0)
    OPEN = BLEGapSecMode(1, 1)
    ENCRYPTION = BLEGapSecMode(1, 2)
    MITM = BLEGapSecMode(1, 3)
    LESC_MITM = BLEGapSecMode(1, 4)
    SIGN_OR_ENCRYPT = BLEGapSecMode(2, 1)
    SIGN_OR_ENCRYPT_MITM = BLEGapSecMode(2, 2)


class BLEGapSecLevels(object):
    def __init__(self, lv1, lv2, lv3, lv4):
        self.lv1 = lv1
        self.lv2 = lv2
        self.lv3 = lv3
        self.lv4 = lv4

    @classmethod
    def from_c(cls, sec_level):
        return cls(lv1=sec_level.lv1,
                   lv2=sec_level.lv2,
                   lv3=sec_level.lv3,
                   lv4=sec_level.lv4)

    def to_c(self):
        sec_level = driver.ble_gap_sec_levels_t()
        sec_level.lv1 = self.lv1
        sec_level.lv2 = self.lv2
        sec_level.lv3 = self.lv3
        sec_level.lv4 = self.lv4
        return sec_level

    def __repr__(self):
        return "{}(lv1={!r}, lv2={!r}, lv3={!r}, lv4={!r})".format(self.__class__.__name__,
                                                                   self.lv1, self.lv2, self.lv3, self.lv4)


class BLEGapSecKeyDist(object):
    def __init__(self, enc_key=False, id_key=False, sign_key=False, link_key=False):
        self.enc_key = enc_key
        self.id_key = id_key
        self.sign_key = sign_key
        self.link_key = link_key

    @classmethod
    def from_c(cls, kdist):
        return cls(enc_key=kdist.enc,
                   id_key=kdist.id,
                   sign_key=kdist.sign,
                   link_key=kdist.link)

    def to_c(self):
        kdist = driver.ble_gap_sec_kdist_t()
        kdist.enc = self.enc_key
        kdist.id = self.id_key
        kdist.sign = self.sign_key
        kdist.link = self.link_key
        return kdist

    def __repr__(self):
        return "{}(enc_key={!r}, id_key={!r}, sign_key={!r}, link_key={!r})".format(
            self.__class__.__name__, self.enc_key, self.id_key, self.sign_key, self.link_key)


class BLEGapSecParams(object):
    def __init__(self, bond, mitm, le_sec_pairing, keypress_noti, io_caps, oob, min_key_size, max_key_size, kdist_own,
                 kdist_peer):
        self.bond = bond
        self.mitm = mitm
        self.le_sec_pairing = le_sec_pairing
        self.keypress_noti = keypress_noti
        self.io_caps = io_caps
        self.oob = oob
        self.min_key_size = min_key_size
        self.max_key_size = max_key_size
        self.kdist_own = kdist_own
        self.kdist_peer = kdist_peer

    @classmethod
    def from_c(cls, sec_params):
        return cls(bond=sec_params.bond,
                   mitm=sec_params.mitm,
                   le_sec_pairing=sec_params.lesc,
                   keypress_noti=sec_params.keypress,
                   io_caps=sec_params.io_caps,
                   oob=sec_params.oob,
                   min_key_size=sec_params.min_key_size,
                   max_key_size=sec_params.max_key_size,
                   kdist_own=BLEGapSecKeyDist.from_c(sec_params.kdist_own),
                   kdist_peer=BLEGapSecKeyDist.from_c(sec_params.kdist_peer))

    def to_c(self):
        sec_params = driver.ble_gap_sec_params_t()
        sec_params.bond = self.bond
        sec_params.mitm = self.mitm
        sec_params.lesc = self.le_sec_pairing
        sec_params.keypress = self.keypress_noti
        sec_params.io_caps = self.io_caps
        sec_params.oob = self.oob
        sec_params.min_key_size = self.min_key_size
        sec_params.max_key_size = self.max_key_size
        sec_params.kdist_own = self.kdist_own.to_c()
        sec_params.kdist_peer = self.kdist_peer.to_c()
        return sec_params

    def __repr__(self):
        return "{}(bond={!r}, mitm={!r}, lesc={!r}, " \
               "keypress_noti={!r}, io_caps={!r}, oob={!r}, " \
               "min_key_size={!r}, max_key_size={!r}, " \
               "kdist_own={!r}, kdist_peer={!r})".format(self.__class__.__name__, self.bond, self.mitm,
                                                         self.le_sec_pairing, self.keypress_noti, self.io_caps,
                                                         self.oob, self.min_key_size, self.max_key_size,
                                                         self.kdist_own, self.kdist_peer)


class BLEGapMasterId(object):
    RAND_LEN = driver.BLE_GAP_SEC_RAND_LEN

    def __init__(self, ediv=0, rand=""):
        self.ediv = ediv
        self.rand = rand

    def to_c(self):
        rand_array = util.list_to_uint8_array(self.rand)
        master_id = driver.ble_gap_master_id_t()
        master_id.ediv = self.ediv
        master_id.rand = rand_array.cast()
        return master_id

    @classmethod
    def from_c(cls, master_id):
        rand = bytearray(util.uint8_array_to_list(master_id.rand, cls.RAND_LEN))
        ediv = master_id.ediv
        return cls(ediv, rand)

    def __repr__(self):
        return "{}(e: {!r}, r: {!r})".format(self.__class__.__name__, self.ediv, binascii.hexlify(self.rand))


class BLEGapEncryptInfo(object):
    KEY_LENGTH = driver.BLE_GAP_SEC_KEY_LEN

    def __init__(self, ltk="", lesc=False, auth=False):
        self.ltk = ltk
        self.lesc = lesc
        self.auth = auth

    def to_c(self):
        info = driver.ble_gap_enc_info_t()
        info.ltk = util.list_to_uint8_array(self.ltk).cast()
        info.lesc = self.lesc
        info.auth = self.auth
        info.ltk_len = len(self.ltk)
        return info

    @classmethod
    def from_c(cls, info):
        ltk = bytearray(util.uint8_array_to_list(info.ltk, cls.KEY_LENGTH))
        lesc = info.lesc
        auth = info.auth
        return cls(ltk, lesc, auth)

    def __repr__(self):
        if not self.ltk:
            return ""
        return "Encrypt(ltk: {}, lesc: {}, auth: {})".format(binascii.hexlify(self.ltk), self.lesc, self.auth)


class BLEGapEncryptKey(object):
    def __init__(self, enc_info=None, master_id=None):
        self.enc_info = enc_info
        self.master_id = master_id

    def to_c(self):
        key = driver.ble_gap_enc_key_t()

        if self.enc_info:
            key.enc_info = self.enc_info.to_c()
        if self.master_id:
            key.master_id = self.master_id.to_c()
        return key

    @classmethod
    def from_c(cls, key):
        enc_info = BLEGapEncryptInfo.from_c(key.enc_info)
        master_id = BLEGapMasterId.from_c(key.master_id)
        return cls(enc_info, master_id)

    def __repr__(self):
        if not self.enc_info:
            return ""
        return "key: {}, master_id: {}".format(self.enc_info, self.master_id)


class BLEGapIdKey(object):
    KEY_LENGTH = driver.BLE_GAP_SEC_KEY_LEN

    def __init__(self, irk="", peer_addr=None):
        self.irk = irk
        self.peer_addr = peer_addr

    def to_c(self):
        irk_key = driver.ble_gap_id_key_t()

        irk = driver.ble_gap_irk_t()
        irk.irk = util.list_to_uint8_array(self.irk).cast()
        irk_key.id_info = irk

        if self.peer_addr:
            addr = self.peer_addr.to_c()
            irk_key.id_addr_info = addr
        return irk_key

    @classmethod
    def from_c(cls, id_key):
        irk = bytearray(util.uint8_array_to_list(id_key.id_info.irk, cls.KEY_LENGTH))
        addr = BLEGapAddr.from_c(id_key.id_addr_info)
        return cls(irk, addr)

    def __repr__(self):
        if not self.irk:
            return ""
        return "irk: {}, peer: {}".format(binascii.hexlify(self.irk), self.peer_addr)


class BLEGapPublicKey(object):
    KEY_LENGTH = driver.BLE_GAP_LESC_P256_PK_LEN

    def __init__(self, key=""):
        self.key = key

    def to_c(self):
        key = driver.ble_gap_lesc_p256_pk_t()
        key.pk = util.list_to_uint8_array(self.key).cast()
        return key

    @classmethod
    def from_c(cls, key):
        key_data = bytearray(util.uint8_array_to_list(key.pk, cls.KEY_LENGTH))
        return cls(key_data)

    def __repr__(self):
        if not self.key:
            return ""
        return binascii.hexlify(self.key)


class BLEGapDhKey(object):
    KEY_LENGTH = driver.BLE_GAP_LESC_DHKEY_LEN

    def __init__(self, key=""):
        self.key = key

    def to_c(self):
        key = driver.ble_gap_lesc_dhkey_t()
        key.key = util.list_to_uint8_array(self.key).cast()

        return key

    @classmethod
    def from_c(cls, key):
        key_data = bytearray(util.uint8_array_to_list(key.key, cls.KEY_LENGTH))
        return cls(key_data)

    def __repr__(self):
        if not self.key:
            return ""
        return binascii.hexlify(self.key)


class BLEGapSignKey(object):
    KEY_LENGTH = driver.BLE_GAP_SEC_KEY_LEN

    def __init__(self, key=""):
        self.key = key

    def to_c(self):
        key = driver.ble_gap_sign_info_t()
        key.csrk = util.list_to_uint8_array(self.key).cast()
        return key

    @classmethod
    def from_c(cls, key):
        key_data = bytearray(util.uint8_array_to_list(key.csrk, cls.KEY_LENGTH))
        return cls(key_data)

    def __repr__(self):
        if not self.key:
            return ""
        return binascii.hexlify(self.key)


class BLEGapSecKeys(object):
    def __init__(self, enc_key=None, id_key=None, sign_key=None, public_key=None):
        if not enc_key:
            enc_key = BLEGapEncryptKey()
        if not id_key:
            id_key = BLEGapIdKey()
        if not sign_key:
            sign_key = BLEGapSignKey()
        if not public_key:
            public_key = BLEGapPublicKey()
        self.enc_key = enc_key        # type: BLEGapEncryptKey
        self.id_key = id_key          # type: BLEGapIdKey
        self.sign_key = sign_key      # type: BLEGapSignKey
        self.public_key = public_key  # type: BLEGapPublicKey

    def to_c(self):
        keys = driver.ble_gap_sec_keys_t()
        keys.p_enc_key = self.enc_key.to_c()
        keys.p_id_key = self.id_key.to_c()
        keys.p_sign_key = self.sign_key.to_c()
        keys.p_pk = self.public_key.to_c()
        return keys

    @classmethod
    def from_c(cls, keys):
        enc_key = BLEGapEncryptKey.from_c(keys.p_enc_key)
        id_key = BLEGapIdKey.from_c(keys.p_id_key)
        sign_key = BLEGapSignKey.from_c(keys.p_sign_key)
        pk = BLEGapPublicKey.from_c(keys.p_pk)
        return cls(enc_key, id_key, sign_key, pk)

    def __repr__(self):
        return "{}(enc: {}, id: {}, sign: {}, pk: {})".format(self.__class__.__name__, self.enc_key, self.id_key,
                                                              self.sign_key, self.public_key)


class BLEGapSecKeyset(object):
    def __init__(self, own_keys=None, peer_keys=None):
        if not own_keys:
            own_keys = BLEGapSecKeys()
        if not peer_keys:
            peer_keys = BLEGapSecKeys()
        self.own_keys = own_keys
        self.peer_keys = peer_keys
        self.ble_keyset = self.to_c()

    def to_c(self):
        self.ble_keyset = driver.ble_gap_sec_keyset_t()
        self.ble_keyset.keys_own = self.own_keys.to_c()
        self.ble_keyset.keys_peer = self.peer_keys.to_c()
        return self.ble_keyset

    def reload(self):
        self.own_keys = BLEGapSecKeys.from_c(self.ble_keyset.keys_own)
        self.peer_keys = BLEGapSecKeys.from_c(self.ble_keyset.keys_peer)

    @classmethod
    def from_c(cls, keyset):
        own_keys = BLEGapSecKeys.from_c(keyset.keys_own)
        peer_keys = BLEGapSecKeys.from_c(keyset.keys_peer)
        return cls(own_keys, peer_keys)

    def __repr__(self):
        return "{}(own: {!r}, peer: {!r})".format(self.__class__.__name__, self.own_keys, self.peer_keys)
