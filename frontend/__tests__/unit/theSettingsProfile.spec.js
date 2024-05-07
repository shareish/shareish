import { mount } from "@vue/test-utils";
import TheSettingsProfile from "@/components/TheSettingsProfile.vue";

describe("TheSettingsProfile", () => {
    it("Test fields of Settings Profile", async () => { 
        
        const wrapper = mount(TheSettingsProfile, {
            mocks: {
                $t: () => {},
                $tc: () => {},
            },
            propsData: {
                user: {
                    description: "description",
                    homepage_url: "homepage_url",
                    facebook_url: "facebook_url",
                    instagram_url: "instagram_url",
                    mastodon_url: "mastodon_url",
                    images : []
                },
            },
        });

        await wrapper.vm.$nextTick();
        expect(wrapper.find("#description").element.value).toBe("description");
        expect(wrapper.find("#homepage_url").element.value).toBe("homepage_url");
        expect(wrapper.find("#facebook_url").element.value).toBe("facebook_url");
        expect(wrapper.find("#instagram_url").element.value).toBe("instagram_url");
        expect(wrapper.find("#mastodon_url").element.value).toBe("mastodon_url");

        wrapper.find("#description").setValue("new description");
        wrapper.find("#homepage_url").setValue("new homepage_url");
        wrapper.find("#facebook_url").setValue("new facebook_url");
        wrapper.find("#instagram_url").setValue("new instagram_url");
        wrapper.find("#mastodon_url").setValue("new mastodon_url");

        await wrapper.vm.$nextTick();
        expect(wrapper.find("#description").element.value).toBe("new description");
        expect(wrapper.find("#homepage_url").element.value).toBe("new homepage_url");
        expect(wrapper.find("#facebook_url").element.value).toBe("new facebook_url");
        expect(wrapper.find("#instagram_url").element.value).toBe("new instagram_url");
        expect(wrapper.find("#mastodon_url").element.value).toBe("new mastodon_url");


        expect(wrapper.vm.internalUser.description).toBe("new description");
        expect(wrapper.vm.internalUser.homepage_url).toBe("new homepage_url");
        expect(wrapper.vm.internalUser.facebook_url).toBe("new facebook_url");
        expect(wrapper.vm.internalUser.instagram_url).toBe("new instagram_url");
        expect(wrapper.vm.internalUser.mastodon_url).toBe("new mastodon_url");
        
    }); 
});