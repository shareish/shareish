import { mount } from "@vue/test-utils";
import TheSettingsProfile from "@/components/TheSettingsProfile.vue";

describe("TheSettingsProfile", () => {
    it("Test fields of Settings Profile", async () => { 
        
        const wrapper = mount(TheSettingsProfile, {
            mocks: {
                $t: () => {},
            },
            propsData: {
                user: {
                },
            },
        });

    });
});