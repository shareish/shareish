import { mount } from '@vue/test-utils';
import TheSettingsNotification from '@/components/TheSettingsNotifications.vue';

jest.mock("@/functions", () => ({
  GeolocationCoords: jest.fn().mockImplementation(() => ({
    longitude: 0,
    latitude: 0,
  }))
}));

describe('TheSettingsNotification', () => {
  it('Test fields of Settings Notification', async () => {
    const wrapper = mount(TheSettingsNotification, {
      mocks: {
        $t: () => {},
      },
      propsData: { 
        user : {
          dwithin_notifications: 20,
          mail_notif_freq_conversations: 'daily',
          mail_notif_freq_events: 'daily',
          mail_notif_freq_items: 'daily',
          mail_notif_freq_osm: 'daily',
          mail_notif_generalinfo: 'daily',
          ref_location: {longitude: 0, latitude: 0},
        },
      },
      data () {
        return {
          address: 'test address',
        }
      }
    });

    expect(wrapper.vm.internalUser['dwithin_notifications']).toBe(20);    
    expect(wrapper.vm.internalUser['mail_notif_freq_conversations']).toBe('daily');
    expect(wrapper.vm.internalUser['mail_notif_freq_events']).toBe('daily');
    expect(wrapper.vm.internalUser['mail_notif_freq_items']).toBe('daily');
    expect(wrapper.vm.internalUser['mail_notif_freq_osm']).toBe('daily');
    expect(wrapper.vm.internalUser['mail_notif_generalinfo']).toBe('daily');
    expect(wrapper.vm.internalUser.ref_location).toStrictEqual({ longitude: 0, latitude: 0 });
    expect(wrapper.vm.address).toBe('test address');
  });
});
